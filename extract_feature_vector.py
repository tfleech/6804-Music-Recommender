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

import hdf5_getters as h5

    """
    This function will return a feature vector containing tempo, danceability, energy,
    loudnes, and year given a path.  The path can be generated using 
    "get_path_from_id."
    """
def get_feature_vector(path):
    song_data = h5.open_h5_file_read(path)
    danceability = h5.get_danceability(song_data)
    energy = h5.get_energy(song_data)
    loudness = h5.get_loudness(song_data)
    tempo = h5.get_tempo(song_data)
    year = h5.get_year(song_data)
    song_data.close()
    return [tempo, danceability, energy, loudness, year]


    """
    Use this to generate the path to a song.  Pass in a track_id which can be found
    from the sqlite database.
    """
def get_path_from_id(id):
    path_to_db = '/media/tom/New Volume/6.804/6804-Music-Recommender/'
    folder1 = id[2]
    folder2 = id[3]
    folder3 = id[4]
    return path_to_db + folder1 + '/' + folder2 + '/' + folder3 + '/' + id + '.h5'


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
dbfile = '/media/tom/New Volume/6.804/6804-Music-Recommender/AdditionalFiles/track_metadata.db'

# connect to the SQLite database
conn = sqlite3.connect(dbfile)

# from that connection, get a cursor to do queries
c = conn.cursor()
#c = conn.execute('select * from tracks')

# so there is no confusion, the table name is 'songs'
TABLENAME = 'songs'


#Use some query to find a track id
q = "SELECT title, track_id FROM songs WHERE artist_name="
q += encode_string('Bob Dylan')
res = c.execute(q)
song = res.fetchone()
print(song[0])

#Generate the path and feature vector for that song
song_path = get_path_from_id(song[1])
song_vec = get_feature_vector(song_path)
print(song_vec)

# close the cursor and the connection
# (if for some reason you added stuff to the db or alter
#  a table, you need to also do a conn.commit())
c.close()
conn.close()