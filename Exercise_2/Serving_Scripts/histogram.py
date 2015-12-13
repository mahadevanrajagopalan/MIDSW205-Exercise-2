#!/usr/bin/python
import sys, getopt, psycopg2

#get number of commandline arguments
nargs = len(sys.argv)

if (nargs==3):
  lb = sys.argv[1]
  ub = sys.argv[2]
  if (lb>ub):
    print 'histogram.py incorrect usage: enter  lowerbound upperbound'
    sys.exit()
else:
  print 'histogram.py incorrect usage: enter  lowerbound upperbound'
  sys.exit()

#connect to the database
conn = psycopg2.connect(database="Tcount",
                        user="postgres",
                        password="pass",
                        host="localhost",
                        port="5432")


#get cursor
cur = conn.cursor()
cur.execute("SELECT word, count from Tweetwordcount where count >={} and count <= {} order by count desc" .format(lb, ub))

#fetch all the words
rec = cur.fetchall()

for r in rec:
  print "{}:{}" .format(r[0], r[1])

conn.commit()

conn.close()

