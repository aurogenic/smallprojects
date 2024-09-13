import math

class Vector:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        if isinstance(other, tuple):
            if len(other) == 2:
                other = Vector(*other)
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        raise NotImplemented
        
    def dot(self, other):
        if not isinstance(other, Vector):
            raise TypeError("only vectors are allowed as Parameter for dot method")
        return (self.x*other.x + self.y*other.y)
    
    __matmul__ = dot

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
        
    __abs__ = magnitu
        
    def __neg__(self):
        return Vector(- self.x, - self.y)
        
    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)
        
    def __sub__(self, other):
        return self + (- other)
        
    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x * other, self.y*other)
        raise NotImplemented
            
    def __rmul__(self, other):
           return self * other
    
    def __truediv__(self, other):
            if isinstance( other, int) or isin
            
    def distance(self, other):
        return abs(self - other)        
    
