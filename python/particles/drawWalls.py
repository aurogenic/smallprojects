#import pygame
from wall import *
from vector import *
from particle import *

particle= Particle(1 , (1,1), 1, (1, 1))

def p(i, j):
    particle.position = Vector(i, j)
    return particle




def draw_vertical_wall(screen, wall, color, width = 1):
    if isinstance(wall, FiniteWall):
        y1 = int(max(0, min(wall.p1.y, wall.p2.y)))
        y2 = int(min(screen.get_height(), max(wall.p1.y, wall.p2.y)))
    else:
        y1 = 0
        y2 = screen.get_height()
    x = int(wall.property[0])
    pygame.draw.line(screen, color, (x ,y1), (x, y2), width)
    
    
    
def draw_horizontal_wall(screen, wall, color, width = 1):
    if isinstance(wall, FiniteWall):
        x1 = int(max(0, min(wall.p1.x, wall.p2.x)))
        x2 = int(min(screen.get_width(), max(wall.p1.x, wall.p2.x)))
    else:
        x1 = 0
        x2 = screen.get_width()
    y = int(wall.property[0])
    pygame.draw.line(screen, color, (x1 ,y), (x2, y), width)
        
        
def draw_linear_wall(screen, wall, color, width = 1):
    if isinstance(wall, FiniteWall):
        x1 = int(wall.p1.x)
        y1 = int(wall.p1.y)
        x2 = int(wall.p2.x)
        y2 = int(wall.p2.y)
    else:
        x1 = 0
        x2 = screen.get_height()
        y1 = int(x1 * wall.property[0] + wall.property[1])
        y2 = int(xw*wall.property[0] + wall.property[1])
    pygame.draw.line(screen, color, (x1 ,y1), (x2, y2), width)


def draw_circular_wall(screen, wall, color, width):
        center , radius = wall.property
        pygame.draw.circle(screen, color, center, radius, width)
        
        
def draw_ellipse_wall(screen, wall, color, width):
        center, a, b = wall.property
        xo , yo = center
        for angle in range(0, 360, 3):
            theta = math.radians(angle)
            x = xo + 2*a*math.cos(theta)
            y = yo + 2*b*math.sin(theta)
            pygame.draw.circle(screen, color, (x, y), width)
        

    
def draw_wall(screen, wall, color, width=10):
    if wall.isa("vertical"):
        draw_vertical_wall(screen, wall, color, width)
    elif wall.isa("horizontal"):
        draw_horizontal_wall(screen, wall, color, width)
    elif wall.isa("linear"):
        draw_horizontal_wall(screen, wall, color, width)
    elif wall.isa("circular"):
        draw_circular_wall(screen, wall, color, width)
    elif wall.isa("ellipse"):
        draw_ellipse_wall(screen, wall, color, width)
        
