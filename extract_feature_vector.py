import os
import sys
import glob
import time
import datetime
import numpy as np
try:
    import sqlite3
except ImportError:
    print('you need sqlite3 installed to use this program')

import hdf5_getters as h5
import csv

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
    #path to million song database
    path_to_db = '/media/tom/New Volume/6.804/database/'
    folder1 = id[2]
    folder2 = id[3]
    folder3 = id[4]
    return path_to_db + folder1 + '/' + folder2 + '/' + folder3 + '/' + id + '.h5'

"""
Finds the squared error between two feature vectors
"""
def se(feature1, feature2):
    return np.sum(np.square(np.subtract(feature1, feature2)))


"""
Adds the titles and feature vectors for a list of songs to a csv file.  This
is used to store a subset of the main database for comparisons later.
"""
def build_csv(titles, features):
    data_to_write = []
    for i in range(len(titles)):
        data_to_write.append([titles[i], features[i][0], features[i][1], features[i][2], features[i][3], features[i][4]])
    myFile = open('song_subset.csv', 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(data_to_write)

"""
Reads in songs stored in csv
"""
def read_csv(csv_file):
    songs = []
    titles = []
    with open(csv_file) as myFile:
        reader = csv.reader(myFile)
        for row in reader:
            titles.append(row[0])
            songs.append([float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5])])
    return [titles, songs]


"""
Finds the mean, variance, and standard deviation for a list of song
feature vectors.  It first regroups the feature vectors to put all
of the same features together in a list.  It then uses numpy and
simple algebra to compute the three values for each feature.
"""
def get_stats_from_song_vec(song_vec):
    feature_lists = [[],[],[],[],[]]
    for i in range(len(song_vec)):
        for j in range(5):
            feature_lists[j].append(song_vec[i][j])

    means = []
    variances = []
    stdevs = []
    for i in range(5):
        means.append(sum(feature_lists[i])/len(feature_lists[i]))
        variances.append(np.var(feature_lists[i], ddof=1))
        stdevs.append(variances[i]**0.5)

    return [means, variances, stdevs]

def encode_string(s):
    """
    Simple utility function to make sure a string is proper
    to be used in a SQLite query
    (different than posgtresql, no N to specify unicode)
    EXAMPLE:
      That's my boy! -> 'That''s my boy!'
    """
    return "'"+s.replace("'","''")+"'"

"""
First, finds the title and track_id for a random sample of
1000 songs using the sqlite database.  Then, it generates
the song vector for the h5 file and returns the titles and
song vectors.
"""
def get_subset(cursor):
    #Select 0.1% (1,000 songs) from the database
    #q = "SELECT title, track_id FROM songs WHERE (ABS(CAST((BINARY_CHECKSUM(*) *RAND()) as int)) % 10000) < 10"
    q = "SELECT title, track_id FROM songs WHERE artist_name="
    q += encode_string('Bob Dylan')
    res = cursor.execute(q)
    songs = res.fetchall()[:4]

    #Generate the path and feature vector for that song
    song_vec = []
    titles = []
    for i in range(len(songs)):
        titles.append(songs[i][0])
        song_path = get_path_from_id(songs[i][1])
        song_features = get_feature_vector(song_path)
        song_vec.append(song_features)

    return [titles, song_vec]

def find_matches(new_vec, titles, song_vec, N):
    suggestions = []
    for n in range(N):
        min_ind = 0;
        min_val = 99999999;
        for i in range(len(song_vec)):
            if se(song_vec[i], new_vec) < min_val:
                min_val = se(song_vec[i], new_vec)
                min_ind = i
        suggestions.append(titles[min_ind])
        titles.pop(min_ind)
        song_vec.pop(min_ind)
    return suggestions

# PATH TO track_metadat.db
#dbfile = '/media/tom/New Volume/6.804/database/AdditionalFiles/track_metadata.db'

# connect to the SQLite database
#conn = sqlite3.connect(dbfile)
#cursor = conn.cursor()
#TABLENAME = 'songs'

"""
Example of sampling database and then building csv for future
use.
"""
#[titles, song_vec] = get_subset(cursor)
#build_csv(titles, song_vec)



[titles, song_vec] = read_csv('song_subset.csv')
print(titles)

[means, variances, stdevs] = get_stats_from_song_vec(song_vec)

print(means)
print(stdevs)

new_vec = [110.0, 0.0, 0.0, -14.0, 1980]
print(find_matches(new_vec, titles, song_vec, 2))

#cursor.close()
#conn.close()

"""
A sample Query and construction of song_vecs and titles

#Use some query to find a track id
q = "SELECT title, track_id FROM songs WHERE artist_name="
q += encode_string('Bob Dylan')
res = c.execute(q)
songs = res.fetchall()[:4]

#Generate the path and feature vector for that song
song_vec = []
titles = []
feature_lists = [[],[],[],[],[]]
for i in range(len(songs)):
    titles.append(songs[i][0])
    song_path = get_path_from_id(songs[i][1])
    song_features = get_feature_vector(song_path)
    song_vec.append(song_features)
"""