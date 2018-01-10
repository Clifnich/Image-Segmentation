# This script is an example of how to interact with image in python
# Please refer to matplotlib.org/users/image_tutorial.html
# for more detailed information

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
img = mpimg.imread('example.png')
imgplot = plt.imshow(img)
lum_img = img[:,:,0]
plt.imshow(lum_img)

plt.show()
