#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""
Implementation of GJK algorithm to detect intersection of convex shapes.

Uses the convexity of Minkowski differences to quickly detect 
intersection of convex shapes.

Extensible to any convex shape as long support function is defined for it.
"""

__author__ = "Abhijit Kale"

from geometry_base import *
from shapes import *



def support(shape1, shape2, direction):
    """Find support for the Minkowski difference in the given direction
    
    PARAMETERS
    ----------
    shape1, shape2: Shape
    The inputs for Minkowski difference. `shape1` is subtracted from `shape2`
    
    direction: Point
    The direction for finding the support
    
    RETURN
    ------
    : Point
    Support for Minkowski difference in the given direction
    """
    return shape1.support(direction) - shape2.support(-direction)

def handle_simplex(simplex, direction):
    
    # If only two points in the simplex (2D), treat it as line case, else triangle case.
    if len(simplex) == 2:
        return line_case(simplex, direction)
    else:
        return triangle_case(simplex, direction)
    
def line_case(simplex, direction):
    BA = Vec(simplex[0], simplex[1])
    BO = Vec(simplex[0], Point(0, 0, 0))
    
    # If the points A, B and O are collinear, the shapes intersect and we are done. 
    if BA.cross(BO).get_length() == 0:
        return True
    
    towards_origin_arrow = triple_prod(BA, BO, BA)
    direction.set_coords(towards_origin_arrow.get_direction()) # Update direction
    
    return False

def triangle_case(simplex, direction):
    A, B, C = simplex
    CB = Vec(C, B)
    CA = Vec(C, A)
    CO = Vec(C, Point(0, 0, 0))
    
    # Find perpendicular arrows for sides CA and CB
    CA_perp_arrow = triple_prod(CB, CA, CA)
    CB_perp_arrow = triple_prod(CA, CB, CB)
    
    if CO.dot(CB_perp_arrow) > 0: # Check if origin contained in outside region swept by side CB
        simplex.remove(A)
        direction.set_coords(CB_perp_arrow.get_direction())
        return False
    elif CO.dot(CA_perp_arrow) > 0: # Check if origin contained in outside region swept by side CA
        simplex.remove(B)
        direction.set_coords(CA_perp_arrow.get_direction())
        return False
    else: # Origin is contained inside the simplex
        return True

def triple_prod(vec1, vec2, vec3):
    """ Triple cross product (vec1 x vec2) x vec3.
     
    PARAMETERS
    ----------
    vec{1, 2, 3}: Vec
    Vectors for triple cross product. Order is important
    """
    cross_vec = vec1.cross(vec2)
    return cross_vec.cross(vec3)

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
    direction = Vec(shape1.get_center(), shape2.get_center()).get_direction()
    A = support(shape1, shape2, direction)
    simplex = [A]
    direction = Vec(simplex[0], Point()).get_direction()

    while True:
        B =  support(shape1, shape2, direction)
        AB = Vec(simplex[0], B)
        
        if dot_direction(AB, direction) <= 0:
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
    