"""
Unit tests for shapes.py module
"""

__author__ = "Abhijit Kale"

import unittest
import sys

from .context import gjk
from gjk.geometry_shapes import *

class TestCircleMethods(unittest.TestCase):
    def setUp(self):
        self.circ = Circle(radius=3, normal=Point(0,0,2))
        
    def test_getters(self):
        self.assertEqual(self.circ.normal, Point(0,0,1))
        
    def test_setters(self):
        with self.assertRaises(ValueError):
            self.circ.radius = -1
    
    def test_support(self):
        for coord1, coord2 in zip(self.circ.support(Point(1,1,1).get_normalized()).coords, (1.73205080756887,1.73205080756887,0)):
            self.assertAlmostEqual(coord1, coord2, places=4)
    

if __name__ == "__main__":
    unittest.main()