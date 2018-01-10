# Test the compute_energy function in optimize_labeling.py
import sys
sys.path.append('../')
import optimize_labeling as opt

import unittest
import numpy as np

debug = True

class TestComputeEnergy(unittest.TestCase):

	 def test0(self):
		  f = np.matrix('80, 160')
		  image = np.matrix('255, 0')
		  self.assertEqual(56305, opt.compute_energy(f, image))

	 def test1(self):
		  f = np.matrix('80, 160; 160, 80')
		  image = np.matrix('255, 0; 0, 255')
		  self.assertEqual(112770, opt.compute_energy(f, image))

if __name__ == '__main__':
	 unittest.main()
