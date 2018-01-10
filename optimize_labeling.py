import numpy as np
import networkx as nx
import math

debug = True
# This function exhausts all the possible
# two-element pairs in a set L
def get_pairs(L):
	 # type check, must be list
	if not isinstance(L, list):
		print('get_pairs method meets a paramter that is not a list')
		return []
	result = []
	for i in range(0, len(L) - 1):
		for j in range(i + 1, len(L)):
				result.append([L[i], L[j]])
	return result

# This function computes the energy for one 
# labeling on the image
def compute_energy(f, image):
	 # compute E_data
	 e_data = np.sum(np.power(f - image, 2))
	
	 # compute E_smooth
	 e_smooth = 0;
	 for i in range(image.shape[0]):
		 for j in range(image.shape[1]):
		    # if j is not the last pixel on one row, add horizontal neighbor
			 if not j == (image.shape[1] - 1):
				  e_smooth += abs(f[i,j] - f[i,j+1])
		    # if i is not the last row, add vertical neighbor
			 if not i == (image.shape[0] - 1):
				 e_smooth += abs(f[i,j] - f[i+1,j])
	 if debug:
	 	 print(str(e_data) + ' ' + str(e_smooth))
	 return e_data + e_smooth

# This function computes the edge weight in the created graph for a pixel and a given label
# label is the label of the terminal that node 'i+3' is currently connected to
def edge_weight(label, pair, i, f, image, width, height):
	 # D_p(\alpha)
	 if debug:
	 	 print('==edge_weight function get label: ' + str(label))
	 	 print('==edge_weight function get i: ' + str(i))
	 	 print('==edge_weight function get f: ')
	 	 print(f)
	 	 print('==end of f')
	 	 print('==edge_weight function gets image: ')
	 	 print(image)
	 	 print('==end of image')
	 	 print('==edge_weight function get width: ' + str(width))
	 	 print('==edge_weight function get height: ' + str(height))
	 d_p = math.pow(label - image[0, i], 2)
	 if debug:
	 	 print('d_p is ' + str(d_p))

	 # find p's neighbors, a vector of indices	 
	 neighbors = []

	 # find neighbors horizontally
	 # if i is the first pixel in a row
	 if i % width == 0:
		  # if i is not the last pixel in a row
		  if (i % width) != width - 1:
		  	  # make sure that added is not in P_alpha beta
		  	  if not f[0, i+1] in pair:
	 		  		  neighbors.append(i+1)
	 else:
		  # if i is not the last pixel in a row
		  if (i % width) != width - 1:
				  neighbors.append(i+1)
		  neighbors.append(i-1)

	 # find neighbors vertically
	 current_height = int(i / width)
	 if current_height == 0:
		  if current_height != height - 1:
	 		  neighbors.append(i + width)
	 else:
		  if current_height != height - 1:
				  neighbors.append(i + width)
		  neighbors.append(i - width)	 

	 # compute the right part of the weight
	 weight = d_p
	 # print('--- neighbors for ' + str(i))
	 # print(neighbors)
	 # print('--- end of neighbors')
	 for neighbor in neighbors:
		 weight += abs(f[0, neighbor] - label) 
	 return weight

# This function updates the labeling f basing on a partition
# Return a updated labeling
def update_labeling(f, group, pair):
	 # if this group has node '1', they should all be labeled beta
	 if '1' in group:
		  for node in group:
			  if node == '1':
					  continue
				# node '3' is actually the first pixel in the labeling, that explains minus three
			  f[0, int(node) - 3] = pair[1]
	 if '2' in group:
		  for node in group:
			  if node == '2':
					 continue
			  f[0, int(node) - 3] = pair[0]
	 return f

# This function finds the labeling with the
# least energy that is within one alpha-beta
# swap of f using graph cut
# And algo update the labeling f
def argmin(pair, image, f):
	width = image.shape[1]
	height = image.shape[0]
	# roll the image and labeling into vectors
	image = image.reshape(1, image.shape[0] * image.shape[1])
	f = f.reshape(1, f.shape[0] * f.shape[1])

	# initialize a graph
	G = nx.Graph()

	# p_alpha_beta is the set for all the pixels that either have label pair[0] or pair[1]
	p_alpha_beta = []
	if debug:
		print('--- pair is ')
		print(pair)
		print('--- end pair')
	# print('f[0]')
	# print(f[0])
	# print('pair[0]')
	# print(pair[0])
	# iterate through each of the pixels
	for i in range(0, image.shape[1]):
	 	# if debug:
	 	
		# skip the pixel if it is neither labeled alpha nor beta
		if f[0,i] != pair[0]:
			if f[0,i] != pair[1]:
				continue

		# add the index to p_alpha_bet
		p_alpha_beta.append(i)

		# the first pixel corresponds to the third node in the graph
		# Here the index is the position of the corresponding node for the pixel
		index = 3 + i

		# add t-links that connect to alpha
		# print('-- edge_weight is')
		# weight = edge_weight(pair[0], i, f, width, height)
		# print(str(index))
		# print(weight)
		# print('-- end of edge_weight')
		weight = edge_weight(pair[0], pair, i, f, image, width, height)
		G.add_edge('1', str(index), capacity = weight)
		if debug:
			print('adding edge 1-' + str(index) +', with weight ' + str(weight))
		# add t-links that connect to beta
		# print(edge_weight(pair[1], i, f, width, height))
		weight = edge_weight(pair[1], pair, i, f, image, width, height)
		G.add_edge('2', str(index), capacity = weight)
		if debug:
			print('adding edge 2-' + str(index) +', with weight ' + str(weight))

	# add n-links
	for i in range(0, len(p_alpha_beta) - 1):
		current_index = p_alpha_beta[i]
		next_index = p_alpha_beta[i+1]
		# if they are neighbors
		if next_index == (current_index + 1):
				G.add_edge(str(current_index + 3), str(next_index + 3), capacity = abs(pair[0] - pair[1]))	

	# apply the min-cut algorithm
	cut_value, partition = nx.minimum_cut(G, '1', '2')
	# divide the partition into two groups
	group1, group2 = partition
	print(partition)
	# update the labeling basing on the minimum cut
	f = update_labeling(f, group1, pair)
	f = update_labeling(f, group2, pair)
	return f, compute_energy(f.reshape(height, width), image.reshape(height, width))

# This function optimizes the energy of a labeling of an image
# It is the core part of the BVP01 algorithm
def optimize_labeling(f, image, L):
	e_f = compute_energy(f, image)
	while (True):
		success = False
		for pair in get_pairs(L):
			f_hat, e_f_hat = argmin(pair, image, f)
			if True:
				print('==optimize_labeling for pair')
				print(pair)
				print('==end of pair')
				print('e_f is: ' + str(e_f))
			if (e_f_hat < e_f):
				f = f_hat
				e_f = e_f_hat
				success = True
		if not success:
			break
	return f
