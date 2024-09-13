from vector import Vector
from particle import *
from pygame import mixer

mixer.init()
mixer.music.load("pop.wav")
mixer.music.set_volume(0.7)

DP = 0.001

class Wall:
    def __init__(self, function, normal, flags = [], p = []):
        self.function = function
        self.normal = normal
        self.flags = flags
        self.property = p
        
    def isa(self, flag):
        return flag in self.flags
        
    def is_in_collision(self, particle, wallwidth=10):
        dist = self.function(particle)
        return abs(dist) <= particle.radius + wallwidth/2, abs(dist)
        
        
    def collide_with_particle(self, particle, wallwidth = 10):
        # V' = V - 2Vp            
        #Vp = component of V perpendicular to curve
        # Vp = (V.n) n
        # n = unit vector normal to curve at point
        
        collision, dist = self.is_in_collision(particle, wallwidth)
        if collision:
            mixer.music.set_volume(abs(particle.velocity)/5000)
            mixer.music.play()
            n = self.normal(particle)
            overlap = particle.radius + wallwidth - dist
            Vp = (particle.velocity @ n)*n
            particle.velocity -= 2*Vp
            if overlap == 0:
                return False
            particle.position += n*(overlap+ DP*overlap/abs(overlap))
            return True
        return False
            
            
            
class FiniteWall(Wall):
        def __init__(self, function, normal, p1, p2, flags=[], property=[]):
            super().__init__(function, normal, flags, property)
            if isinstance(p1, Vector):
                self.p1 = p1
                self.p2 = p2
            else:
                self.p1 = Vector(*p1)
                self.p2 = Vector(*p2)
            
        def binds(self, particle):
           #Q is closest point to P on line AB
           # checks if Q is within A and B
           AB = self.p2 - self.p1
           AP = particle.position - self.p1
           wall_length = abs(AB)
           projection = (AP @  AB) / wall_length
           Q = self.p1 + AB*projection/wall_length
           return -particle.radius <= projection<= wall_length+particle.radius, Q
           
        def is_in_collision(self , particle, wallwidth=10):
           binds, Q = self.binds(particle)
           if binds:
               dist = abs(particle.position - Q)
               return dist <= particle.radius + wallwidth/2, Q
           return False, None
           
        def collide_with_particle(self, particle, wallwidth= 10):
           colliding, Q = self.is_in_collision(particle, wallwidth)
           if colliding:
                
               mixer.music.set_volume(abs(particle.velocity)/5000)
               mixer.music.play()
               PQ = particle.position - Q
               overlap = particle.radius + wallwidth - abs(PQ)
               n = PQ / abs(PQ)
               Vp = (particle.velocity @ n) *n
               particle.velocity -= 2*Vp
               if overlap == 0:
                   return False
               particle.position += n*(overlap+DP*overlap/abs(overlap))
               return True
           return False
               
               

               
               
def vertical_wall(x):
    # x = c, y = y
    def funct(particle):
        return particle.position.x - x
    def norm(particle):
        # unit vector pointing +ve x axis
        return Vector(1, 0)
    return Wall(funct, norm, ["vertical"], [x])
    
def horizontal_wall(y):
    # y = c, x = x
    def funct(particle):
        return particle.position.y - y
    def norm(particle):
        return Vector(0, 1)
    return Wall(funct, norm, ["horizontal"], [y])
    
def linear_wall(slope, intercept):
    #y = ax + b
    #y = mx + c
    def funct(particle):
        return particle.position.y - (slope*particle.position.x + intercept)
    def norm(particle):
        return Vector(-slope, 1).direction()
    return Wall(funct, norm, ["linear"], [slope, intercept])

def finite_wall(wall: Wall, p1, p2):
    if isinstance(p1, tuple):
        p1 = Vector(*p1)
        p2 = Vector(*p2)
    return FiniteWall(wall.function, wall.normal, p1, p2, wall.flags, wall.property)
    
def infinte_wall(wall: Wall):
    return Wall(wall.function, wall.normal, wall.flags, wall.property)
    
def vertical_segment_wall(x, y1, y2):
    p1 = Vector(x, y1)
    p2 = Vector(x, y2)
    wall = vertical_wall(x)
    return finite_wall(wall, p1, p2)
    
def horizontal_segment_wall(y, x1, x2):
    p1 = Vector(x1, y)
    p2 = Vector(x2, y)
    wall = horizontal_wall(y)
    return finite_wall(wall, p1, p2)
    
def segment_wall(p1, p2):
    p1 = Vector(*p1)
    p2 = Vector(*p2)
    dy = p2.y - p1.y
    if dy == 0:
        return horizontal_segment_wall(p1.y, p1.x, p2.x)
    dx = p2.x - p1.x
    if dx == 0:
        return vertical_segment_wall(p1.x, p1.y, p2.y)
    slope = dy / dx
    intercept = p1.y - slope*p1.x
    wall = linear_wall(slope, intercept, "linear", [slope, intercept])
    return finite_wall(wall, p1, p2)
    
def circular_wall(center, radius):
    def funct(particle):
        dx = particle.position.x - center[0]
        dy = particle.position.y - center[1]
        return math.sqrt(dx**2 + dy**2 ) - radius
    def norm(particle):
        dx = particle.position.x - center[0]
        dy = particle.position.y - center[1]
        dist = math.sqrt(dx**2 + dy**2)
        return Vector(dx / dist, dy /dist)
    return Wall(funct, norm, ["circular"], [center, radius])
    
def ellipse_wall(center, a, b):
    def funct(particle):
        x = particle.position.x - center[0]
        y = particle.position.y - center[1]
        return (x**2/a**2) + (y**2/b**2) - 1
    def norm(particle):
        dx = particle.position.x - center[0]
        dy = particle.position.y - center[1]
        dist = math.sqrt((2*dx / a**2)**2 + (2*dy / b**2)**2)
        return Vector(2*dx / a**2 / dist, 2*dy / b**2 /dist)
    return Wall(funct, norm, ["ellipse"], [center, a,  b])
    
    
def parabolic_wall(a, b, c):
        def funct(particle):
            return particle.position.y - a*particle.position.x**2 - b*particle.position.x - c
        def norm(particle):
            dx = -2*a*particle.position.x - b
            dy = 1
            return Vector(dx,  dy).direction()
        return wall(function, norm, ["quadratic", "parabola"], [a, b, c])
        
        
def sinewave_wall(amp, freq, phase = 0):
        def funct(particle):
            return particle.position.y - amp*math.sin(freq*particle.position.x + phase)
        def norm(particle):
            dx = - amp*freq*math.cos(freq*particle.position.dx + phase)
            dy = 1
            return Vector(dx, dy).direction()
        return wall(funct, norm, ["sinewave"], [amo, freq, phase])
        
class  Scaling_Circle(Wall):
    def __init__(self, rad, pos, scale, color):
        self.radius = rad
        self.position = Vector(*pos)
        self.scale = scale
        self.color = color
        self.flags = ["circular"]
        self.property = [pos, rad]
        
    def isa(self, p):
       return super().isa(p)
       
    def is_in_collission(self, particle, wallwidth= 1):
       dist = particle.position - self.position
       return abs(dist) > self.radius - particle.radius-wallwidth/2, dist
       
    def collide_with_particle(self, particle, wallwidth = 1):
       colliding,  n = self.is_in_collission(particle, wallwidth)
       if colliding:
             n.normalize()
             if self.radius>particle.radius:
                self.radius *= self.scale
                mixer.music.set_volume(abs(particle.velocity)/5000)
                mixer.music.play()
                limit = self.radius - particle.radius - wallwidth/2
                self.property[1] *= self.scale
                Vp = (particle.velocity @ n) * n
                particle.velocity -= 2*Vp
                particle.position = self.position + n*limit
                return True
       return False