import sys
sys.path.append('../')

import optimize_labeling as opt

import numpy as np

f = np.matrix('80, 100; 160, 80')
image = np.matrix('255, 0;0,255')
opt.optimize_labeling(f, image, [80, 100, 160])
