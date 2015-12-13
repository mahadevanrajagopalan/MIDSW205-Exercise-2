#Start postgresql 

service postgresql initdb
service postgresql restart

#Change password of user postgres to be "pass"

sudo -u postgres psql
postgres=#\password
Enter new password: pass
Enter it again:
postgres=#control-D

cd /var/lib/pgsql/data

#edit pga_hba.conf
#change settings for local connection to password other and connections  to TRUST from IDENT

#restart service
service postgresql restart

#Create the Tcount database

sudo -u postgres createdb -O postgres -h localhost -p 5432 Tcount

#confirm database Tcount exists
psql -U postgres

postgres=#\l

#It should show the Tcount db

# Environment setup
# I'm assuming that this application is being run in an AMI instance similar to # ucbw205_complete_plus_postgres_PY2.7.
# install streamparse following directions from lab 9

# install tweepy and psycopg2
cd 
pip install psycopg2
pip install tweepy

#Create EX2Tweetwordcount project
sparse quickstart EX2Tweetwordcount

# Next configure the storm topology
cd  EX2Tweetwordcount
cd topologies

mv worcount.clj wordcount.clj.bak


#Create tweetwordcount.clj by copying changes from the git repository sub-folder topologies

# Setup spouts
cd ../src/spouts

mv wordcount.py wordcount.py.bak
#copy tweets.py from the github repository subfolder src/spouts into this directory

#setup bolts
cd ../src/bolts
mv wordcount.py wordcount.py.bak

#copy parse.py and wordcount.py from the repository subfolder src/bolts into this  directory


# Now actually try to run everything.
cd EX2Tweetwordcount
sparse run

# observe the wordcount bolt emit the word counts.

# copy the serving database scripts from the Serving_Scripts folder in the respository.
# In another terminal copy the serving scripts, finalresults.py and histogram.py to the top level project # directory and run them in any way you desire.

# Emit the number of occurrences of hello in the twitter stream
python finalresults.py hello

# all the words and their counts in the serving database sorted alphabetically
python finalresults.py
#histogram of the words
python histogram.py 1  5


