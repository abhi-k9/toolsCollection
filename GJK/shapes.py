"""
Shape library for GJK algorithm
"""

__author__ = "Abhijit Kale"

from geometry_base import Point, dot_dir_dir

class Shape:
    """Interface for shape objects"""
    
    def __init__(self):
        pass
    
    @property
    def center(self):
        pass
    
    def support(self, direction):
        """Find the support for the shape in the given direction
        
        PARAMETERS
        ----------
        direction: Point
        The direction for finding the support
        
        RETURN
        ------
        : Point
        Support in the given direction
        """
        pass
    

class Circle(Shape):
    def __init__(self, radius, normal=Point(0,0,1), center=Point(0,0,0)):
        self.center = center
        self.radius = radius
        self.normal = normal
    
    @property
    def center(self):
        return self._center
    @center.setter
    def center(self, c):
        self._center = c
    
    @property    
    def radius(self):
        return self._radius
    @radius.setter
    def radius(self, r):
        if r < 0:
            raise ValueError("Radius must be positive")
        else:
            self._radius = r
    
    @property
    def normal(self):
        return self._normal
    @normal.setter
    def normal(self, n):
        self._normal = n.get_normalized()
    
    def support(self, direction):
        projected_direction = direction - direction*dot_dir_dir(self._normal, direction)
        return self.center + projected_direction*self._radius
    

class Sphere(Shape):
    def __init__(self, radius, center=Point(0,0,0)):
        self.center = center
        self.radius = radius
    
    @property
    def center(self):
        return self._center
    @center.setter
    def center(self, c):
        self._center = c
    
    @property    
    def radius(self):
        return self._radius
    @radius.setter
    def radius(self, r):
        if r < 0:
            raise ValueError("Radius must be positive")
        else:
            self._radius = r
    
    def support(self, direction):
        return self.center + direction*self.radius
        

class Cuboid(Shape):
    def __init__(self, height, width, depth=0, center=Point(0,0,0)):
        self._center = center # by-pass setter method, since it calls calc_vertices which needs both `_center` and `_dims` attributes to be set.
        self.dims = (height, width, depth)
        self.calc_vertices()
    
    @property
    def dims(self):
        return self._dims
    @dims.setter
    def dims(self, dim):
        h, w, d = dim
        if h < 0 or w < 0 or d < 0:
            raise ValueError(f"Dimensions must be positive. Given height={h}, width={w}, depth={d}")
        else:
            self._dims = (h, w, d)
            self.calc_vertices()
    
    @property 
    def vertices(self):
        return self._vertices
    @vertices.setter
    def vertices(self):
        raise AttributeError("Cannot set vertices directly. Please set dimensions and center instead.")
    
    @property
    def center(self):
        return self._center
    @center.setter
    def center(self, c):
        self._center = c
        self.calc_vertices()
     
    def calc_vertices(self):
        cx, cy, cz = self.center.coords
        delta_x, delta_y, delta_z = (dim/2 for dim in self.dims)
        
        top_z, bottom_z = cz+delta_z, cz-delta_z 
        
        self._vertices = [self.get_face_vertices(cx, cy, top_z, delta_x, delta_y),
                         self.get_face_vertices(cx, cy, bottom_z, delta_x, delta_y)]
    
    def get_face_vertices(self, c1, c2, c3, delta_1, delta_2): # order: tr, tl, br, bl
        face_vertices = [Point(c1+delta_1, c2+delta_2, c3),
                        Point(c1-delta_1, c2+delta_2, c3),
                        Point(c1+delta_1, c2-delta_2, c3),
                        Point(c1-delta_1, c2-delta_2, c3)]
        return face_vertices
    
    def support(self, direction):
        d_x, d_y, d_z = direction.coords
        vertices = self.vertices
        
        face = vertices[0] if d_z >0 else vertices[1]
        side = face[:2] if d_y > 0 else face[2:]
        vertex = side[0] if d_x > 0 else side[1]
        
        return vertex
    
