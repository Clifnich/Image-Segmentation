# This script tests the functionality of get_neighbors()
import sys 
sys.path.append('../')
import alpha_expansion as alp

import unittest
import numpy as np

debug = True

class TestGetNeighbors(unittest.TestCase):

	 def test0(self):
		  image = np.matrix('0,255,255,0')
		  neighbors = alp.get_neighbors(image, 2, 2)
		  if debug:
				 print(neighbors)
		  self.assertEqual(4, len(neighbors))

	 def test1(self):
		  image = np.matrix('0,255')
		  neighbors = alp.get_neighbors(image, 1, 2)
		  if debug:
				 print(neighbors)
		  self.assertEqual(1, len(neighbors))

if __name__ == '__main__':
    unittest.main()
