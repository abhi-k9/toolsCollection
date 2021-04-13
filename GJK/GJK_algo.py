#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implementation of GJK algorithm to detect intersection of convex shapes.

Uses the convexity of Minkowski differences to quickly detect 
intersection of convex shapes.

Extensible to any convex shape as long as a support function is defined for it.

Inspired from https://www.youtube.com/watch?v=ajv46BSqcK4
"""

__author__ = "Abhijit Kale"

from geometry_base import *
from shapes import *

def support(shape1, shape2, direction):
    """Find support for the Minkowski difference in the given direction.
    
    PARAMETERS
    ----------
    shape1, shape2: Shape
    The inputs for Minkowski difference. `shape1` is subtracted from `shape2`.
    
    direction: Point
    The direction for finding the support.
    
    RETURN
    ------
    : Point
    Support for Minkowski difference in the given direction.
    """
    return shape1.support(direction) - shape2.support(-direction)

def handle_simplex(simplex, direction):
    """ Dispatch simplex processing to the correct handler. 
    
    PARAMETERS
    ----------
    simplex: list(Point)
    
    direction [out]: Point
    New direction to look for support.
    
    RETURN
    ------
    : bool
    `True` if shapes intersect, otherwise update the direction towards the origin and return `False`.
    """
    
    # If only two points in the simplex (2D), treat it as line case, else triangle case.
    if len(simplex) == 2:
        return line_case(simplex, direction)
    else:
        return triangle_case(simplex, direction)
    
def line_case(simplex, direction):
    """ Handles degenerate simplex (a line in 2D).
    
    PARAMETERS
    ----------
    simplex: list(Point)
    
    direction [out]: Point
    New direction to look for support.
    
    RETURN
    ------
    : bool
    `True` if shapes intersect, otherwise update the direction towards the origin and return `False`.
    """
    BA = Vec(simplex[0], simplex[1])
    BO = Vec(simplex[0], Point(0, 0, 0))
    
    # If the points A, B and O are collinear, the shapes intersect and we are done. 
    if BA.cross(BO).length == 0:
        return True
    
    towards_origin_arrow = triple_prod(BA, BO, BA) # Arrow towards origin. (non-normalized directions)
    direction.coords = towards_origin_arrow.direction # Update direction
    
    return False

def triangle_case(simplex, direction):
    """ Handles non-degenerate simplex case (triangle in 2D).
    
    PARAMETERS
    ----------
    simplex: list(Point)
    
    direction [out]: Point
    New direction to look for support.
    
    RETURN
    ------
    `True` if shapes intersect, otherwise update the direction towards the origin and return `False`.
    """
    A, B, C = simplex
    CB = Vec(C, B)
    CA = Vec(C, A)
    CO = Vec(C, Point(0, 0, 0))
    
    # Find perpendicular arrows (non-normalized directions) for sides CA and CB
    CA_perp_arrow = triple_prod(CB, CA, CA)
    CB_perp_arrow = triple_prod(CA, CB, CB)
    
    if CO.dot(CB_perp_arrow) > 0: # Check if origin contained in outside region swept by side CB
        simplex.remove(A)
        direction.coords = CB_perp_arrow.direction
        return False
    elif CO.dot(CA_perp_arrow) > 0: # Check if origin contained in outside region swept by side CA
        simplex.remove(B)
        direction.coords = CA_perp_arrow.direction
        return False
    else: # Origin is contained inside the simplex
        return True

def GJK(shape1, shape2):
    """ Implementation of the GJK algorithm
    
    PARAMETERS
    ----------
    shape{1, 2}: Shape
    
    RETURN
    ------
    : bool
    Signifies if the given shapes intersect or not.
    """

    # Initialize algorithm parameters
    direction = Vec(shape1.center, shape2.center).direction
    A = support(shape1, shape2, direction)
    simplex = [A]
    direction = Vec(simplex[0], Point()).direction

    while True: # while new valid support found. `direction` is updated each iteration.
        B =  support(shape1, shape2, direction)
        AB = Vec(simplex[0], B)
        
        if dot_vec_dir(AB, direction) <= 0: # No support past the origin
            return False
        else:
            simplex.append(B)
        
        if handle_simplex(simplex, direction):
            return True
    

if __name__ == "__main__":
    
    s1 = Sphere(radius = 5 ,center=Point(10,10))
    s2 = Cuboid(height=5 , width=5, depth=5 , center=Point())
    
    if GJK(s1, s2):
        print("Shapes intersect.")
    else:
        print("Shapes do NOT intersect.")
    