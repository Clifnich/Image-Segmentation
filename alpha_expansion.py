# This script is an implementation of alpha-expansion algorithm of BVP 2001 paper.
# You can see that it is highly similar in structure with the alpha-beta swap algorithm implemented in optimize_labeling.py
# The naming may be confusing because both optimize_labeling.py and this alpha_expansion.py are all labeling optimization scripts. They are basically of the same function, but with different core components. So just be aware of it, as for users, each of the algorithm is fine.

# This function optimizes the energy of a labeling of an image
# It is the basic structure of the BVP01 algorithm

import optimize_labeling as opt
import networkx as nx
import math

# whether we want to print debug message
debug = True

# This function computes the weight of a specified edge
#def edge_weight():
#	 return 0
# This function computes the index for a pixel in the flat-version of image
def pixel2index(pixel, width):
#	 print('pixel is')
#	 print(pixel)

	 return pixel[0] * width + pixel[1]

# Given a position, this function returns 4 neighbors of the pixel.
# Right up, down, left and right. 
# 4-neighborhood system
def get4neighbors(row, col):
	 neighbors = []
	 neighbors.append([row-1, col])
	 neighbors.append([row+1, col])
	 neighbors.append([row, col-1])
	 neighbors.append([row, col+1])
	 if debug:
		  print('below is get4neighbors')
		  print(neighbors)
	 return neighbors

# This function gets all the neighboring pairs in an image
# here we are assuming the algorithm requires the 4-neighborhood system
def get_neighbors(image, height, width):
	 if debug:
		  print('image shape is: ')
		  print(image.shape)
		
	 neighbors = []
	 for i in range(0, image.shape[1]):
		  # which row the current pixel is in, counting from 0
		  row = int(i / width)
		  # which column the current pixel is in, counting from 0
		  col = i % width
		  for pixel in get4neighbors(row, col):
				 row1, col1 = pixel
				 # if the pixel's position is valid
				 if row1 >= 0 and row1 < height and col1 >= 0 and col1 < width:
					 # add it as a neighbor
					 neighbor_pair = [[row, col], [row1, col1]]
					 reverse_pair = [[row1, col1], [row, col]]
					 # make sure that such a neighboring pair is not added before
					 if not neighbor_pair in neighbors and not reverse_pair in neighbors:
						  if debug:
								 print('adding a neighbor_pair')
								 print(neighbor_pair)
						  neighbors.append(neighbor_pair)
	 return neighbors

# This function updates the labeling, the specification is still pending for edition. 
def update_labeling(f, group, label):
	 if '1' in group:
		  print('ERROR! you should not use group 1 to update the labeling, they should stay the same according to the paper')
		  return f
	 if debug:
		  print('group is:')
		  print(group)
	 for node in group:
		  # skip the hat alpha node
		  if node == '2':
				  continue
		  # skip the auxiliary nodes
		  if '_' in node:
				  continue
		  index = int(node) - 3
		  print('changing pixel ' + str(index) + ' to label ' + str(label))
		  f[0, index] = label
	 return f

# This function finds the labeling with the
# least energy that is within one alpha-beta
# swap of f using graph cut
# And algo update the labeling f
# NOTE: like in the alpha-beta swap case, here we assume that image and f are two 'flat' variables, which means that they are one row matrices
def argmin(alpha, image, f):
	 # alpha corresponds to node #1 in the graph
	 # alpha_hat, node #2
	 # the numbering of the pixels start from #3, so the first pixel corresponds to #3, the second #4
	 # The auxiliary nodes are numbered by their neighbors, for example, for an auxiliary node between node #3 and node #4, it is refered to as node #3_4 in the graph
	 width = image.shape[1]
	 height = image.shape[0]
	 # convert alpha to an integer
	 alpha = int(alpha)
	 # roll the image and labeling into vectors
	 image = image.reshape(1, image.shape[0] * image.shape[1])
	 f = f.reshape(1, f.shape[0] * f.shape[1])

	 # initialize the graph
	 G = nx.Graph()

	 # add all the t-links
	 for i in range(0, image.shape[1]):
		  # get the index of the node ready, so that the first pixel will correspond to the third node in the graph, or node #3
		  index = i + 3
		  if debug:
				 print('alpha is ' + str(alpha))
				 print(image)
				 print(image[0, i])
				 print('adding a t-link 1-' + str(index) + ', with weight ' + str(math.pow(alpha - image[0, i], 2)))
		  # add all the t-links with respect to alpha
		  G.add_edge('1', str(index), capacity = math.pow(alpha - image[0, i], 2))
		  # add all the t-links with respect to alpha_hat
		  if f[0, i] == alpha:
				 # if pixel p has label alpha, empty capacity means infinity
				 if debug:
					 print('adding a t-link 2-' + str(index) + ', with infinity weight')
				 G.add_edge('2', str(index))
		  else:
				 if debug:
					 print('adding a t-link 2-' + str(index) + ', with weight ' + str(math.pow(f[0, i] - image[0, i], 2)))
				 G.add_edge('2', str(index), capacity = math.pow(f[0, i] - image[0, i], 2))

	 # add all the n-links and edges for the auxiliary nodes
	 for pair in get_neighbors(image, height, width):
		  # we get all the neighboring pairs from the image
		  # index1 is the index of the first pixel from the pair in the graph
		  if debug:
				 print('===line 114, here is a pair')
				 print(pair)
				 print(pair[0][0])
				 print(pair[0][1])
		  # convert to a flat-version of index
		  index1 = pair[0][0] * width + pair[0][1] + 3
		  # index2 is the index of the second pixel from the pair in the graph
		  index2 = pair[1][0] * width + pair[1][1] + 3
		  if debug:
				 print('index1 is: ' + str(index1) + ', index2 is ' + str(index2))
		  
		  # if they have the same labels, add an n-link
		  if f[0, index1 - 3] == f[0, index2 - 3]:
				 # the pair computation may look ugly
				 weight = abs(f[0, pixel2index(pair[0], width)] - alpha)
				 if debug:
					 print('adding a n-link ' + str(index1) + '-' + str(index2) + ', with weight ' + str(weight))
				 G.add_edge(str(index1), str(index2), capacity = weight)
		  # if they don't have the same labels, add a triplet of edges
		  # add all the edges related to the auxiliary nodes
		  else:
				 if debug:
					 print('adding an auxiliary node')
				 auxiliary_node_index = str(index1) + '_' + str(index2)
				 index0 = pixel2index(pair[0], width)
				 index1 = pixel2index(pair[1], width)
				 G.add_edge(str(index1), auxiliary_node_index, capacity = abs(f[0, index0] - alpha))
				 G.add_edge(str(index2), auxiliary_node_index, capacity = abs(f[0, index1] - alpha))
				 G.add_edge('2', auxiliary_node_index, capacity = abs(f[0, index0] - f[0, index1]))

	 # apply the min-cut algorithm
	 cut_value, partition = nx.minimum_cut(G, '1', '2')
	 # divide the partition into two groups
	 group1, group2 = partition
	 if debug:
		  print(partition)
	 # update the labeling based on the minimum cut, we only need to update the pixels that are assigned to the second group because the first group will stay the same as is stated in the paper
	 f = update_labeling(f, group2, alpha)

	 return f, opt.compute_energy(f.reshape(height, width), image.reshape(height, width))

def optimize_labeling(f, image, L):
	e_f = opt.compute_energy(f, image)
	while (True):
		success = False
		for label in L:
			f_hat, e_f_hat = argmin(label, image, f)
			if debug:
				print('==optimize_labeling for pair')
				print(label)
				print('==end of pair, e_f is: ' + str(e_f))
			if (e_f_hat < e_f):
				f = f_hat
				e_f = e_f_hat
				success = True
				break
		if not success:
			break
	return f
