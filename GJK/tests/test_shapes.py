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
        self.assertEqual(self.circ.normal, Point(0,0,1)) # Check if setter normalizes the given normal
        
    def test_setters(self):
        with self.assertRaises(ValueError):
            self.circ.radius = -1
    
    def test_support(self):
        for test_coord, verified_coord in zip(self.circ.support(Point(1,1,1).get_normalized()).coords, (2.1213203435596424,2.1213203435596424,0)):
            self.assertAlmostEqual(test_coord, verified_coord, places=4)
    

class TestSphereMethods(unittest.TestCase):
    def setUp(self):
        self.sphere = Sphere(radius=3)
    
    def test_support(self):
        for test_coord, verified_coord in zip(self.sphere.support(Point(1,1,1).get_normalized()).coords, (1.73205080756887,1.73205080756887,1.73205080756887)):
            self.assertAlmostEqual(test_coord, verified_coord, places=4)

    def test_setters(self):
        with self.assertRaises(ValueError):
            self.sphere.radius = -1

class TestCuboidMethods(unittest.TestCase):
    def setUp(self):
        self.cuboid = Cuboid(height=3, width=3, depth=6)
        
    def test_getters(self):
        verified_vertices = [
            [Point(*[1.5, 1.5, 3.0]), Point(*[-1.5, 1.5, 3.0]), Point(*[1.5, -1.5, 3.0]), Point(*[-1.5, -1.5, 3.0])], 
            [Point(*[1.5, 1.5, -3.0]), Point(*[-1.5, 1.5, -3.0]), Point(*[1.5, -1.5, -3.0]), Point(*[-1.5, -1.5, -3.0])]
        ]
        self.assertEqual(self.cuboid.vertices, verified_vertices)
    
    def test_support(self):
        for test_coord, verified_coord in zip(self.cuboid.support(Point(1,1,1).get_normalized()).coords, (1.5,1.5,3)):
            self.assertAlmostEqual(test_coord, verified_coord, places=4)
    
    def test_setters(self):
        with self.assertRaises(ValueError):
            self.cuboid.dims = (-1, 0, 0)
        with self.assertRaises(ValueError):
            self.cuboid.dims = (0, -1, 0)
        with self.assertRaises(ValueError):
            self.cuboid.dims = (0, 0, -1)

        self.cuboid.dims = (1,2,3)
        verified_vertices = [
            [Point(*[0.5, 1.0, 1.5]), Point(*[-0.5, 1.0, 1.5]), Point(*[0.5, -1.0, 1.5]), Point(*[-0.5, -1.0, 1.5])], 
            [Point(*[0.5, 1.0, -1.5]), Point(*[-0.5, 1.0, -1.5]), Point(*[0.5, -1.0, -1.5]), Point(*[-0.5, -1.0, -1.5])]
        ]
        self.assertEqual(self.cuboid.vertices, verified_vertices)

        self.cuboid.center = Point(1,2,3)
        verified_vertices = [
            [Point(*[1.5, 3.0, 4.5]), Point(*[0.5, 3.0, 4.5]), Point(*[1.5, 1.0, 4.5]), Point(*[0.5, 1.0, 4.5])], 
            [Point(*[1.5, 3.0, 1.5]), Point(*[0.5, 3.0, 1.5]), Point(*[1.5, 1.0, 1.5]), Point(*[0.5, 1.0, 1.5])]
        ]
        self.assertEqual(self.cuboid.vertices, verified_vertices)


if __name__ == "__main__":
    unittest.main()