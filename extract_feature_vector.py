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

def se(feature1, feature2):
    return np.square(np.subtract(feature1, feature2))


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

c = conn.cursor()
TABLENAME = 'songs'

#Query to select sample of rows
'''
SELECT * FROM Table1
WHERE (ABS(CAST(
(BINARY_CHECKSUM(*) *
RAND()) as int)) % 100) < 10
'''

#Use some query to find a track id
q = "SELECT title, track_id FROM songs WHERE artist_name="
q += encode_string('Bob Dylan')
res = c.execute(q)
songs = res.fetchall()[:4]
#print(songs)

#Generate the path and feature vector for that song
song_vec = []
#This is a master list
feature_lists = [[],[],[],[],[]]
for i in range(len(songs)):
    song_path = get_path_from_id(songs[i][1])
    song_features = get_feature_vector(song_path)
    song_vec.append(song_features)
    for j in range(5):
        feature_lists[j].append(song_features[j])

means = []
variances = []
stdevs = []
for i in range(5):
    means.append(sum(feature_lists[i])/len(feature_lists[i]))
    variances.append(np.var(feature_lists[i], ddof=1))
    stdevs.append(variances[i]**0.5)

print(means)
print(stdevs)

# close the cursor and the connection
# (if for some reason you added stuff to the db or alter
#  a table, you need to also do a conn.commit())
c.close()
conn.close()