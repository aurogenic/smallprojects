
import pygame
from pygame.locals import *
from particle import Particle
from wall import *
from vector import Vector
from drawWalls import *


try:
    import android
    andr = True
except ImportError:
    andr = False

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 64, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN=(0, 155, 155)
HIGHLIGHT = GREEN
BACKGROUND = BLACK

device = pygame.display.Info()

FPS = 60
DIRECTION = 1
SPEED = 1
dt = DIRECTION * SPEED /FPS
SLOWMOFACTOR = 0.1
SPEEDFACTOR = 2
WIDTH = 800
HEIGHT = 800
WALLWIDTH = 5
BOXPADDING = 50
TEXTHEIGHT = 25
FONT1 =  pygame.font.SysFont('comicsan', TEXTHEIGHT)
GRAVITY = Vector(0, 2000)
def G(position):
    return GRAVITY



WALLRAD = int(WALLWIDTH/2   - 0.5)

xmin = ymin = BOXPADDING - WALLRAD
xmax = WIDTH-BOXPADDING - WALLRAD
ymax = HEIGHT-BOXPADDING- WALLRAD

def check_bounds(particle):
    xlow = xmin + particle.radius
    xhigh = xmax - particle.radius
    ylow = ymin + particle.radius
    yhigh = ymax - particle.radius
    if particle.position.x < xlow:
        particle.position.x = xlow
    elif particle.position.x > xhigh:
        particle.position.x = xhigh
    if particle.position.y < ylow:
        particle.position.y = ylow
    elif particle.position.y > yhigh:
        particle.position.y = yhigh
        
def display(screen, text, pos, color=HIGHLIGHT, font = FONT1):
    surf = font.render(text, True,  color)
    screen.blit(surf, pos)
    

TOPBORD = horizontal_segment_wall(ymin, xmin, xmax)
BOTBORD = horizontal_segment_wall(ymax, xmin, xmax)
LEFBORD= vertical_segment_wall(xmin, ymax, ymin )
RIGBORD = vertical_segment_wall(xmax, ymax, ymin)

CONTAINER = [TOPBORD, BOTBORD, LEFBORD, RIGBORD]
    

screen = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN if andr else 0)
pygame.display.set_caption("Particle Simulation")

clock = pygame.time.Clock()

p1 = Particle(mass = 5, pos=(20,20), rad=5, vel=(100,5), color = GREEN)


particles = [p1]
np = len(particles)


static_walls = CONTAINER
dynamic_walls = []

circle = Scaling_Circle(rad= 100, pos=(int(WIDTH/2), int(HEIGHT/2)), scale= 299/300,color= HIGHLIGHT)
dynamic_walls.append(circle)

line = segment_wall((WIDTH/4, 3*HEIGHT/4), (3*WIDTH/4, 3*HEIGHT/4))
static_walls.append(line)

#ellipse = ellipse_wall((int(WIDTH/2), int(HEIGHT/2)), 100, 50)
#static_walls.append(ellipse)

walls = static_walls + dynamic_walls

wallsurface = pygame.Surface((WIDTH ,HEIGHT))

wallsurface.fill(BACKGROUND)
for wall in static_walls:
   draw_wall(wallsurface, wall, HIGHLIGHT, WALLWIDTH)

def subframe_update(particle):
    particle.update_trails()
    n = int (abs(particle.velocity)*dt / (particle.radius + WALLWIDTH)) + 1
    for _ in range(n):
        particle.update(dt/n, G)
        particle.check_collision(particles, walls)
        check_bounds(particle)

running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key is pygame.K_SPACE or event.key == pygame.K_DOWN:
                SPEED = SLOWMOFACTOR
            if event.key is pygame.K_LCTRL or event.key == pygame.K_RIGHT:
                SPEED = SPEEDFACTOR
            if event.key is pygame.K_LSHIFT or event.key == pygame.K_LEFT:
                DIRECTION = - 1

            dt = DIRECTION * SPEED / FPS
                
        if event.type == KEYUP:
            if event.key is pygame.K_SPACE or event.key == pygame.K_DOLLAR:
                SPEED = 1.0
            if event.key is pygame.K_LCTRL or event.key == pygame.K_RIGHT:
                SPEED = 1.0
            if event.key is pygame.K_LSHIFT or event.key == pygame.K_LEFT:
                DIRECTION = 1.0
            dt = DIRECTION * SPEED / FPS

        elif event.type == FINGERDOWN:
            dt = SLOWMOFACTOR/ FPS
        elif event.type == FINGERUP:
            dt = DIRECTION * SPEED / FPS

    
    screen.blit(wallsurface, (0,0))
        
    for particle in particles:
        subframe_update(particle)
        particle.draw(screen, HIGHLIGHT)
        
    
    for wall in dynamic_walls:
       draw_wall(screen, wall, HIGHLIGHT, WALLWIDTH)
            
    for i in range(np):  
        display(screen, str(particles[i]), (xmin +  TEXTHEIGHT, ymax-(np-i+1)*TEXTHEIGHT)  ,particles[i].color)
    
    
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
