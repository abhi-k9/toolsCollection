"""
Shape library for GJK algorithm
"""

__author__ = "Abhijit Kale"

from geometry_base import Point, dot_direction_direction

class Shape:
    """Interface for shape objects"""
    
    def __init__(self):
        pass
    
    def get_center(self):
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
        self._center = center
        
        if radius < 0:
            raise ValueError("Radius must be positive")
        else:
            self._radius = radius
            self._normal = normal.get_normalized()
        
    def get_center(self):
        return self._center
        
    def get_radius(self):
        return self._radius
    
    def get_normal(self):
        return self._normal
        
    def support(self, direction):
        projected_direction = direction - direction*dot_direction_direction(self._normal, direction)
        return self.get_center() + projected_direction*self.get_radius()
    

class Sphere(Shape):
    def __init__(self, radius, center=Point(0,0,0)):
        self._center = center
        
        if radius < 0:
            raise ValueError("Radius must be positive")
        else:
            self._radius = radius
    
    def get_center(self):
        return self._center
        
    def get_radius(self):
        return self._radius

    def support(self, direction):
        return self.get_center() + direction*self.get_radius()
        

class Cuboid(Shape):
    def __init__(self, height, width, depth=0, center=Point(0,0,0)):
        self._center = center
        if height >= 0 or width >= 0 or depth >= 0:
            self._height = height
            self._width = width 
            self._depth = depth
            self.corners()
        else:
            raise ValueError(f"Dimensions must be positive. Given height={height}, width={width}, depth={depth}")
    
    def get_center(self):
        return self._center
        
    def get_height(self):
        return self._height
    
    def get_width(self):
        return self._width
    
    def get_depth(self):
        return self._width
        
    def get_dim(self):
        return (self._height, self._width, self._depth)
        
    def get_face_corners(self, c1, c2, c3, delta_1, delta_2): # order: tr, tl, br, bl
        face_corners = [Point(c1+delta_1, c2+delta_2, c3),
                        Point(c1-delta_1, c2+delta_2, c3),
                        Point(c1+delta_1, c2-delta_2, c3),
                        Point(c1-delta_1, c2-delta_2, c3)]
        return face_corners
    
    def corners(self):
        cx, cy, cz = self._center.get_coords()
        delta_x, delta_y, delta_z = (dim/2 for dim in self.get_dim())
        
        top_z, bottom_z = cz+delta_z, cz-delta_z 
        
        self._corners = [self.get_face_corners(cx, cy, top_z, delta_x, delta_y),
                         self.get_face_corners(cx, cy, bottom_z, delta_x, delta_y)]   
    
    def get_corners(self):
        return self._corners
        
    def support(self, direction):
        d_x, d_y, d_z = direction.get_coords()
        corners = self.get_corners()
        
        face = corners[0] if d_z >0 else corners[1]
        side = face[:2] if d_y > 0 else face[2:]
        vertex = side[0] if d_x > 0 else side[1]
        
        return vertex
    
