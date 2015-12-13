from __future__ import absolute_import, print_function, unicode_literals
import itertools, time
import tweepy, copy
import Queue, threading
import psycopg2

from streamparse.spout import Spout

################################################################################
# Twitter credentials
################################################################################
twitter_credentials = {
    "consumer_key"        :  "74dgq1cyvMXe7Ll52hTIMIL0x",
    "consumer_secret"     :  "I53EJlz15MzzUV23meVOxuDSQvwmdci6V8MHIFaLsF7JFaEk8S",
    "access_token"        :  "139377964-qiuWyeWTtmgrkOBblySTRBLkd2dRkTpaCEDru36O",
    "access_token_secret" :  "UFtTLjOxIRBcxf2djbGm72Ql36Nfx5w6FJNEOelMr1rKh",
}

def auth_get(auth_key):
    if auth_key in twitter_credentials:
        return twitter_credentials[auth_key]
    return None

def ascii_string(s):
  return all(ord(c) < 128 for c in s)


################################################################################
# Class to listen and act on the incoming tweets
################################################################################
class TweetStreamListener(tweepy.StreamListener):

    def __init__(self, listener):
        self.listener = listener
        super(self.__class__, self).__init__(listener.tweepy_api())

    def on_status(self, status):

# Print tweets for screenshot
#       if (ascii_string(status.text)):
#         print('Stream Object:' + status.text)

        self.listener.queue().put(status.text, timeout = 0.01)
        return True

    def on_error(self, status_code):
        return True # keep stream alive

    def on_limit(self, track):
        return True # keep stream alive

class Tweets(Spout):

    def initialize(self, stormconf, context):
        self._queue = Queue.Queue(maxsize = 100)

        consumer_key = auth_get("consumer_key")
        consumer_secret = auth_get("consumer_secret")
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        if auth_get("access_token") and auth_get("access_token_secret"):
            access_token = auth_get("access_token")
            access_token_secret = auth_get("access_token_secret")
            auth.set_access_token(access_token, access_token_secret)

        # Connect to the database Tcount and create the tweetwordcount table.
        conn = psycopg2.connect(database="Tcount", user="postgres",
                                                      password="pass", host="localhost", port="5432")
        # Get the cursor
        cur = conn.cursor()

        #Drop the table if it already exists
        cur.execute("DROP TABLE  IF EXISTS Tweetwordcount")
        conn.commit()

        # Now create the tweetwordcount table
        # The table has two columns named word and count to hold the words in
        # the tweet as well as the number of occurrences of that word in the
        # tweet stream
        cur.execute("CREATE TABLE  Tweetwordcount (word TEXT PRIMARY KEY  NOT NULL, count INT     NOT NULL);")
        conn.commit()

        self._tweepy_api = tweepy.API(auth)
        #Create the listener for twitter stream
        listener = TweetStreamListener(self)

        # Create the stream and listen for english tweets
        stream = tweepy.Stream(auth, listener, timeout=None)
        stream.filter(languages=["en"], track=["a", "the", "i", "you", "u"], async=True)

    def queue(self):
        return self._queue

    def tweepy_api(self):
        return self._tweepy_api

    def next_tuple(self):
        try:
            tweet = self.queue().get(timeout = 0.1)
            if tweet:
                # Print for screenshot
                #if (ascii_string(tweet)):
                # self.log("Spout: next_tuple: tweet: " + tweet)

                self.queue().task_done()
                self.emit([tweet])

        except Queue.Empty:
            self.log("Empty queue exception ")
            time.sleep(0.1)

    def ack(self, tup_id):
        pass  # if a tuple is processed properly, do nothing

    def fail(self, tup_id):
        pass  # if a tuple fails to process, do nothing



