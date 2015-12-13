from __future__ import absolute_import, print_function, unicode_literals
import psycopg2

from collections import Counter
from streamparse.bolt import Bolt


class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.counts = Counter()

    def process(self, tup):
        word = tup.values[0]

        # Replace ' with \' to escape the apostrophe
        word1 = word.replace('\'','\\\'')

        # Increment the number of occurrences of the word
        self.counts[word1] += 1

        # Connect to the database to store the count of the number of
        # occurrences of the word.
        conn = psycopg2.connect(database="Tcount", user="postgres",
                                password="pass", host="localhost", port="5432")
        cur = conn.cursor()
        # Insert if it is the first occurrence of the word and
        # otherwise update the count in the database table

        # Check if the word exists in the table
        cur.execute("SELECT COUNT(*) from Tweetwordcount WHERE word=\'{}\'" .format(word1))

        if cur.fetchone()[0] > 0:
          # word exists and so update the count
          cur.execute("UPDATE Tweetwordcount SET count={} WHERE word=\'{}\'" .format(self.counts[word1], word1))
        else:
          # word does not exist and so insert the word into the table
          cur.execute("INSERT into Tweetwordcount(word, count) values(\'{0}\',{1})" .format(word1, self.counts[word1]))
        conn.commit()
        self.emit([word1, self.counts[word1]])
        self.log('bolt:WordCounter:%s: %d' % (word1, self.counts[word1]))

