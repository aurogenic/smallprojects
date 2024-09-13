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
        return False
        
    def __str__(self):
        return "x: " + str(round(self.x, 2)).zfill(8) + ", y: " + str(round(self.y, 2)).zfill(8)
        
    def dot(self, other):
        if isinstance(other, tuple):
            return (self.x*other[0] + self.y*other[1])
        if not isinstance(other, Vector):
            raise TypeError("only vectors are allowed as Parameter for dot method")
        return (self.x*other.x + self.y*other.y)
    
    __matmul__ = dot

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
        
    __abs__ = magnitude
        
    def __neg__(self):
        return Vector(- self.x, - self.y)
        
    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)
        
    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)
        
    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x * other, self.y*other)
        raise NotImplemented
            
    def __rmul__(self, other):
           return self * other
    
    def __truediv__(self, other):
            if isinstance( other, int) or isinstance(other, float):
                return self * (1/other)
            
    def distance(self, other):
        return abs(self - other)    
        
    def normalize(self):
        mg = self.__abs__()
        if mg != 0:
            self.x /= mg
            self.y /= mg
        
    def copy(self):
        return Vector(self.x, self.y)
        
    def direction(self):
        temp = self.copy()
        temp.normalize()
        return temp
    
