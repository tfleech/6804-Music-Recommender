import os
import sys
import glob
import time
import datetime
import numpy as np
try:
    import sqlite3
except ImportError:
    print 'you need sqlite3 installed to use this program'
    sys.exit(0)



def encode_string(s):
    """
    Simple utility function to make sure a string is proper
    to be used in a SQLite query
    (different than posgtresql, no N to specify unicode)
    EXAMPLE:
      That's my boy! -> 'That''s my boy!'
    """
    return "'"+s.replace("'","''")+"'"

# PATH TO track_metadat.db
# CHANGE THIS TO YOUR LOCAL CONFIGURATION
# IT SHOULD BE IN THE ADDITIONAL FILES
# (you can use 'subset_track_metadata.db')
dbfile = '/media/tom/New Volume/6.804/MillionSongSubset/AdditionalFiles/subset_artist_similarity.db'

# connect to the SQLite database
conn = sqlite3.connect(dbfile)

# from that connection, get a cursor to do queries
#c = conn.cursor()
c = conn.execute('select * from artists')

# so there is no confusion, the table name is 'songs'
TABLENAME = 'songs'

names = list(map(lambda x: x[0], c.description))
print(names)

#q = "SELECT sql FROM songs WHERE name="
#q += encode_string('Touch the Sky')
#res = c.execute(q)
#print res.fetchall()

# close the cursor and the connection
# (if for some reason you added stuff to the db or alter
#  a table, you need to also do a conn.commit())
c.close()
conn.close()