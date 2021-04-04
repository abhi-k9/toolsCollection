"""
Defines basic geometric entities and operations.
"""

__author__ = "Abhijit Kale"

import math

class Point:
    """Represents a point in 3D space"""
    
    def __init__(self, x=0, y=0, z=0):
        self._coords = [x, y, z]
    
    def get_coords(self):
        return self._coords
    
    def set_coords(self, x , y, z):
        self._coords[:] = x, y, z
    
    def set_coords(self, point):
        self._coords[:] = point.get_coords()
        
    def get_distance(self):
        if hasattr(self, "_distance"): # Return if already exists.
            return self._distance
        else: # Evaluate and return.
            self._distance = 0
            for coord in self.get_coords():
                self._distance += coord**2
            self._distance = math.sqrt(self._distance)
            return self._distance
    
    def get_normalized(self):
        if hasattr(self, "_direction"): # Return if already exists.
            return self._direction
        else:
            self._direction = Point(*(coord/self.get_distance() for coord in self.get_coords()))
            return self._direction
    
    def __neg__(self):
        return Point(*(-coord for coord in self.get_coords()))
    
    def __add__(self, other_point):
        return Point(*(coord1+coord2 for coord1, coord2 in zip(self.get_coords(), other_point.get_coords())))
    
    def __sub__(self, other_point):
        return self + (-other_point)
    
    def __mul__(self, magnitude):
        return Point(*(coord*magnitude for coord in self.get_coords()))
    
    def __repr__(self):
        return f"Point(*{self._coords})"
    

class Vec:
    """Represents a vector in 3D space.
    
    Internally stored as a start point and end point pair.
    """
    
    def __init__(self, start_point=Point(0,0,0), end_point=Point(0,0,0)):
        self._start = start_point
        self._end = end_point
    
    def get_start(self):
        return self._start
    
    def get_end(self):
        return self._end
    
    def get_length(self):
        
        if hasattr(self, "_length"): # Return if already exists.
            return self._length
        else: # Evaluate and return.
            self._length = 0
            for (s, e) in zip(self._start.get_coords(), self._end.get_coords()):
                self._length += (e-s)**2
            self._length = math.sqrt(self._length)
            return self._length
        
    def get_direction(self):
        """Get vector direction.
        
        Represented by a point on unit sphere.
        
        RETURN
        ------
        : Point
        """
        
        if hasattr(self, "_direction"): # Return if already exists.
            return self._direction
        else: # Evaluate and return.
            self._direction = Point(*((e-s)/self.get_length() for (s, e) in zip(self._start.get_coords(), self._end.get_coords()))) #TODO: length could go to zero
            return self._direction
    
    def dot(self, vec):
        """Dot product with another vector
        
        PARAMETERS
        ----------
        vec: Vec
        """
        return dot_direction(self, vec.get_direction())
        
    def cross(self, vec):
        """Cross product with another vector
        
        PARAMETERS
        ----------
        vec: Vec
        """
        self_arrow = self.get_end() - self.get_start() 
        vec_arrow = vec.get_end() - vec.get_start()
        
        s_x, s_y, s_z = self_arrow.get_coords()
        v_x, v_y, v_z = vec_arrow.get_coords()
        
        cross_coords = [s_y*v_z - s_z*v_y,
                        s_z*v_x - s_x*v_z,
                        s_x*v_y - s_y*v_x]
                        
        return Vec(Point(0, 0, 0), Point(*cross_coords))
        
    def __repr__(self):
        return f"Vec({self.get_start()}, {self.get_end()})"
    

def dot_direction_direction(direction1, direction2):
     return sum((dir_coord1*dir_coord2 for dir_coord1, dir_coord2 in zip(direction1.get_coords(), direction2.get_coords())))

def dot_direction(vec, direction):
    """ Evaluates the dot prooduct of a vector with a direction.
    
    PARAMETERS
    ----------
    vec: Vec
    
    direction: Point
    
    RETURN
    ------
    : float
    """
    return sum(((end_coord-start_coord)*dir_coord for start_coord, end_coord, dir_coord in zip(vec.get_start().get_coords(), vec.get_end().get_coords(), direction.get_coords())))
    
def triple_prod(vec1, vec2, vec3):
    """ Triple cross product (vec1 x vec2) x vec3.
     
    PARAMETERS
    ----------
    vec{1, 2, 3}: Vec
    Vectors for triple cross product. Order is important
    """
    cross_vec = vec1.cross(vec2)
    return cross_vec.cross(vec3)