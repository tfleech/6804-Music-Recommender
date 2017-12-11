import matplotlib.pyplot as plt
import numpy as np
import random
import copy

Gaussians = {'bpm': [100, 5], 'vocals': [20, 2], 'guitar': [15, 3], 'drums': [80, 10], 'bass': [35, 4]}

user_input = {'bpm': [110, 9], 'vocals': [18, 7], 'guitar': [15, 8], 'drums': [95, 9], 'bass': [33, 2]}
user_input2 = {'bpm': [130, 7], 'vocals': [17, 5], 'guitar': [20, 4], 'drums': [85, 8], 'bass': [30, 6]}

def se(feature1, feature2):
	s = 0
	for key in feature1:
		s += (feature1[key] - feature2[key])**2
	return s

def update_song_dist(initial_dist, user_input):
	new_dist = copy.deepcopy(initial_dist)
	for key in initial_dist:
		for i in range(user_input[key][1]*50):
			new_dist[key].append(user_input[key][0])
	return new_dist

def sample_dist(dist, samples):
	new_feature = {'bpm': 0, 'vocals': 0, 'guitar': 0, 'drums': 0, 'bass': 0}
	for i in range(samples):
		for key in new_feature:
			new_feature[key] += (float(random.choice(dist[key]))/samples)
	for key in new_feature:
		new_feature[key] = int(new_feature[key])
	return new_feature

initial_dist = {'bpm': [], 'vocals': [], 'guitar': [], 'drums': [], 'bass': []}
for key in initial_dist:
	for i in range(1000):
		initial_dist[key].append(int(np.random.normal(Gaussians[key][0], Gaussians[key][1], 1)))


orig_feature = sample_dist(initial_dist, 1000)
song_dist = update_song_dist(initial_dist, user_input)
song_dist = update_song_dist(song_dist, user_input2)
new_feature = sample_dist(song_dist, 1000)

print(orig_feature)
print(new_feature)
print(se(orig_feature, new_feature))

#plt.hist(song_dist)
#plt.show()