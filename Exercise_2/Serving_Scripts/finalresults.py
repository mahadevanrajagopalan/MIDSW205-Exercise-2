#!/usr/bin/python
import sys, getopt, psycopg2

#get number of commandline arguments
nargs = len(sys.argv)

if (nargs==2):
  word = sys.argv[1]
  uword = word.replace('\'','\\\'')
  allwords=0
elif (nargs > 2):
  print 'incorrect usage: Enter only 1 word as argument'
  sys.exit()
else:
  allwords=1

#connect to the database
conn = psycopg2.connect(database="Tcount", user="postgres",
                        password="pass", host="localhost", port="5432")

#get cursor
cur = conn.cursor()
if (allwords==0):
  cur.execute("SELECT word, count from Tweetwordcount where word='{0}'" .format(uword))
  r = cur.fetchone()
  if (r):
    print "Total number of occurrences of \"{}\":{}\n" .format(r[0],r[1])
  else:
    print "Total number of occurrences of \"{}\":{}\n" .format(uword, 0)
else:
  cur.execute("SELECT word, count from Tweetwordcount order by word asc")
  rec = cur.fetchall()
  for r in rec:
    print "({},{})," .format(r[0], r[1]),
  else:
    print "No Words"

conn.commit()

conn.close()
