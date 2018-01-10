# set the sys path up one level in order to import optimize_labeling
import sys
sys.path.append('../')
import optimize_labeling as opt

import unittest

debug = True

class TestGetPairs(unittest.TestCase):

	 def test0(self):
		  pairs = opt.get_pairs([1,1])
		  self.assertEqual(1, len(pairs))

	 def test1(self):
		  pairs = opt.get_pairs([1,2,3])
		  self.assertEqual(3, len(pairs))

	 def test2(self):
		  pairs = opt.get_pairs([1,2,3,4])
		  self.assertEqual(6, len(pairs))

	 # test elements in details
	 def test3(self):
		  pairs = opt.get_pairs([1,1])
		  pair = pairs[0]
		  if debug:
				  print(pair)
		  self.assertEqual(2, len(pair))

if __name__ == '__main__':
    unittest.main()
