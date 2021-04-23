"""
Defines basic geometric entities and operations.
"""

__author__ = "Abhijit Kale"

import math

class Point:
    """Represents a point in 3D space"""
    
    def __init__(self, x=0, y=0, z=0):
        self._coords = [x, y, z]
    
    @property
    def coords(self):
        return self._coords
        
    @coords.setter
    def coords(self, *args):
        if len(args) == 3:
            self.set_coords_from_coords(*args)
        elif len(args) == 1:
            self.set_coords_from_point(*args)
        else:
            raise RuntimeError("Wrong number of arguments. Expecting a point or three coords.")
    
    def set_coords_from_coords(self, x, y, z):
        self._coords[:] = x, y, z
    def set_coords_from_point(self, point):
        self._coords[:] = point.coords
    
    @property
    def distance(self):
        if hasattr(self, "_distance"): # Return if already exists.
            return self._distance
        else: # Evaluate and return.
            self._distance = 0
            for coord in self.coords:
                self._distance += coord**2
            self._distance = math.sqrt(self._distance)
            return self._distance
    
    def get_normalized(self):
        if hasattr(self, "_direction"): # Return if already exists.
            return self._direction
        else:
            self._direction = Point(*(coord/self.distance for coord in self.coords))
            return self._direction
    
    def __eq__(self, other_point):
        return True if self.coords == other_point.coords else False
    
    def __neg__(self):
        return Point(*(-coord for coord in self.coords))
    
    def __add__(self, other_point):
        return Point(*(coord1+coord2 for coord1, coord2 in zip(self.coords, other_point.coords)))
    
    def __sub__(self, other_point):
        return self + (-other_point)
    
    def __mul__(self, magnitude):
        return Point(*(coord*magnitude for coord in self.coords))
    
    def __abs__(self):
        return Point(*(abs(coord) for coord in self.coords))
    
    def __round__(self, ndigits=0):
        return Point(*(round(coord, ndigits) for coord in self.coords))
        
    def __repr__(self):
        return f"Point(*{self._coords})"
    

class Vec:
    """Represents a vector in 3D space.
    
    Internally stored as a start point and end point pair.
    """
    
    def __init__(self, start=Point(0,0,0), end=Point(0,0,0)):
        self._start = start
        self._end = end
    
    @property
    def start(self):
        return self._start
    @start.setter
    def start(self, s):
        self._start = s
    
    @property
    def end(self):
        return self._end
    @end.setter
    def end(self, e):
        self._end = e
    
    @property
    def length(self):
        if hasattr(self, "_length"): # Return if already exists.
            return self._length
        else: # Evaluate and return.
            self._length = 0
            for (s, e) in zip(self.start.coords, self.end.coords):
                self._length += (e-s)**2
            self._length = math.sqrt(self._length)
            return self._length
    
    @property    
    def direction(self):
        """Get vector direction.
        
        Represented by a point on unit sphere.
        
        RETURN
        ------
        : Point
        """
        if hasattr(self, "_direction"): # Return if already exists.
            return self._direction
        else: # Evaluate and return.
            self._direction = Point(*((e-s)/self.length for (s, e) in zip(self.start.coords, self.end.coords))) #TODO: length could go to zero
            return self._direction
    
    def dot(self, vec):
        """Dot product with another vector
        
        PARAMETERS
        ----------
        vec: Vec
        """
        return dot_vec_dir(self, vec.direction)
    
    def cross(self, vec):
        """Cross product with another vector
        
        PARAMETERS
        ----------
        vec: Vec
        """
        self_arrow = self.end - self.start 
        vec_arrow = vec.end - vec.start
        
        s_x, s_y, s_z = self_arrow.coords
        v_x, v_y, v_z = vec_arrow.coords
        
        cross_coords = [s_y*v_z - s_z*v_y,
                        s_z*v_x - s_x*v_z,
                        s_x*v_y - s_y*v_x]
                        
        return Vec(Point(0, 0, 0), Point(*cross_coords))
    
    def __repr__(self):
        return f"Vec({self.start}, {self.end})"
    

def dot_dir_dir(direction1, direction2):
    """ Evaluates the dot product of a direction with another direction.
    
    PARAMETERS
    ----------
    direction{1, 2}: Point
    
    RETURN
    ------
    : float
    """
    return sum((dir_coord1*dir_coord2 for dir_coord1, dir_coord2 in zip(direction1.coords, direction2.coords)))

def dot_vec_dir(vec, direction):
    """ Evaluates the dot product of a vector with a direction.
    
    PARAMETERS
    ----------
    vec: Vec
    
    direction: Point
    
    RETURN
    ------
    : float
    """
    return sum(((end_coord-start_coord)*dir_coord for start_coord, end_coord, dir_coord in zip(vec.start.coords, vec.end.coords, direction.coords)))

def triple_prod(vec1, vec2, vec3):
    """ Triple cross product (vec1 x vec2) x vec3.
     
    PARAMETERS
    ----------
    vec{1, 2, 3}: Vec
    Vectors for triple cross product. Order is important
    """
    cross_vec = vec1.cross(vec2)
    return cross_vec.cross(vec3)