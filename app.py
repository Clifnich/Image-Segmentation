# This is a image processing application
# You can input an image, set the label 
# set size and expect to see the image 
# separated into several parts as you specified

# import the necessary packages
import matplotlib.pyplot as plt
# I'm using another image library
#import matplotlib.image as mpimg
import numpy as np
import random
from scipy import misc
import time

# import my own scripts
import optimize_labeling as opt
import alpha_expansion as alp

# This function randomizes the labeling of the image
# Return a labeling
def randomize_labeling(image, L):
	 f = np.zeros((image.shape[0], image.shape[1]))
	 for i in range(0, image.shape[0]):
		  for j in range(0, image.shape[1]):
				  f[i,j] = L[random.randint(0, len(L)-1)]
	 print('\n===random labeling')
	 print(f)
	 print('===end of random labeling\n')
	 return f

# This function processes the image based on the labeling f
def process(image, f):
	 for i in range(0, image.shape[0]):
		  for j in range(0, image.shape[1]):
				  #image[i,j] = 255 if f[i,j] == 80 else 0
				  image[i,j] = f[i,j]
	 return image

# L is the set of all labels
#L = [40, 80, 100, 140, 180, 220]
#L = list(range(10, 200, 10))
L = [1, 254]
#print(L)
image = misc.imread('images/lion_clip.png')
print(image.shape)
# convert a RGB image to a grayscale
tmp = np.zeros((image.shape[0], image.shape[1]))
for i in range(0, image.shape[0]):
	for j in range(0, image.shape[1]):
		# for some picture, you might want to change it to image[i,j,0]
		tmp[i, j] = image[i, j, 0]
image = tmp
#print(image.shape)
# optimize the labeling using the predefined functions
tic = time.clock()
# here you can choose which algorithm to use, opt.optimize_labeling uses alpha-beta swap and alpha_expansion uses alpha-expansion
f = opt.optimize_labeling(randomize_labeling(image, L), image, L)
#f = alp.optimize_labeling(randomize_labeling(image, L), image, L)
toc = time.clock()

# process the image base on the new labeling
image = process(image, f.reshape(image.shape[0], image.shape[1]))

# plot the process image
plt.imshow(image)
plt.show()

print(str(toc - tic) + 's.')
