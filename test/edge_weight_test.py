# This script test the edge_weight function
import sys
sys.path.append('../')
import optimize_labeling as opt

import unittest
import numpy as np

debug = False

class TestEdgeWeight(unittest.TestCase):

	 def test0(self):
		  f = np.matrix('80, 160')
		  image = np.matrix('255, 0')
		  pair = [80, 160]
		  self.assertEqual(30625, int(opt.edge_weight(80, [80, 160], 0, f, image, 2, 1)))

if __name__ == '__main__':
	 unittest.main()
