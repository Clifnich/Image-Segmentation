# This script test the argmin function of the alpha_expansion algorithm
# It is quite different from the alpha-beta swap algorithm.

import sys 
sys.path.append('../')
import alpha_expansion as alp 

import unittest
import numpy as np

debug = False

class TestAlphaExpansionArgmin(unittest.TestCase):

	def test0(self):
		f = np.matrix('80, 160')
		image = np.matrix('255, 0')
		label = '80'
		f, e_f = alp.argmin(label, image, f)
		self.assertEqual(80, f[0,1])
		self.assertEqual(80, f[0,0])

	# test on a 1x2 image where two pixels are labeled the same
	def test1(self):
		f = np.matrix('1,1')
		image = np.matrix('0, 255')
		label = 1
		f, e_f = alp.argmin(label, image, f)
		self.assertEqual(64517, e_f)
		  
if __name__ == '__main__':
	unittest.main()
