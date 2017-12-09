import matplotlib.pyplot as plt
import numpy as np
import random

Gaussians = {'bpm': [100, 5], 'vocals': [20, 2], 'guitar': [15, 3], 'drums': [80, 10], 'bass': [35, 4]}

song_dist = {'bpm': [], 'vocals': [], 'guitar': [], 'drums': [], 'bass': []}

for key in song_dist:
	for i in range(1000):
		song_dist[key].append(int(np.random.normal(Gaussians[key][0], Gaussians[key][1], 1)))

user_input = {'bpm': [110, 9], 'vocals': [18, 7], 'guitar': [15, 8], 'drums': [95, 9], 'bass': [33, 2]}


for key in song_dist:
	for i in range(user_input[key][1]*50):
		song_dist[key].append(user_input[key][0])


new_feature = {'bpm': 0, 'vocals': 0, 'guitar': 0, 'drums': 0, 'bass': 0}
for i in range(1000):
	for key in new_feature:
		new_feature[key] += (float(random.choice(song_dist[key]))/1000)
for key in new_feature:
	new_feature[key] = int(new_feature[key])

print(new_feature)

#plt.hist(initial_dist)
#plt.show()