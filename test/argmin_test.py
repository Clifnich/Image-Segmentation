# Test the argmin function which is the core part of this algorithm
import sys
sys.path.append('../')
import optimize_labeling as opt

import unittest
import numpy as np

debug = False

class TestArgMin(unittest.TestCase):

	 def test0(self):
		  f = np.matrix('80, 160')
		  image = np.matrix('255, 0')
		  pair = [80, 160]
		  f, e_f = opt.argmin(pair, image, f)
		  self.assertEqual(160, f[0,0])
		  self.assertEqual(80, f[0,1])
		  self.assertEqual(15505, e_f)
	 
	 def test1(self):
		  f = np.matrix('80, 160; 160, 80')
		  image = np.matrix('255, 0; 0, 255')
		  pair = [80, 160]
		  f, e_f = opt.argmin(pair, image, f)
		  self.assertEqual(160, f[0,0])
		  self.assertEqual(80, f[0,1])
		  self.assertEqual(80, f[0,2])
		  self.assertEqual(160, f[0,3])

if __name__ == '__main__':
	 unittest.main()
