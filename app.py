# This is a image processing application
# You can input an image, set the label 
# set size and expect to see the image 
# separated into several parts as you specified

# import the necessary packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import random

# import my own scripts
import optimize_labeling as opt

# This function randomizes the labeling of the image
# Return a labeling
def randomize_labeling(image, L):
	 f = np.zeros((image.shape[0], image.shape[1]))
	 for i in range(0, image.shape[0]):
		  for j in range(0, image.shape[1]):
				  f[i,j] = random.randint(0, len(L)-1)
	 return f

# This function processes the image based on the labeling f
def process(image, f):
	 for i in range(0, image.shape[0]):
		  for j in range(0, image.shape[1]):
				  image[i,j] = 255 if f[i,j] == 80 else 0
	 return image

# L is the set of all labels
L = [80, 160]
image = mpimg.imread('lion.png')
# convert a RGB image to a grayscale
tmp = np.zeros((image.shape[0], image.shape[1]))
for i in range(0, image.shape[0]):
	for j in range(0, image.shape[1]):
		tmp[i, j] = image[i,j,0]
image = tmp
print(image.shape)
# optimize the labeling using the predefined functions
f = opt.optimize_labeling(image, randomize_labeling(image, L), L)

# process the image base on the new labeling
image = process(image, f)

# plot the process image
plt.imshow(image)
plt.show()
