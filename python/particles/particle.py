from vector import *
import pygame

from pygame import mixer

mixer.init()
mixer.music.load("hit.wav")
mixer.music.set_volume(0.7)

DP = 0.001
class Particle:
    
    def __init__(self, mass = 1, pos = (0, 0), rad = 1, vel = (0,0), color = None):
        self.mass = mass
        self.position = Vector(*pos)
        self.radius = rad
        self.velocity = Vector(*vel) 
        self.color = color
        self.trail = [pos]*20
        
    def momentum(self):
        return self.mass * self.velocity
        
    def kinetic_energy(self):
        return self.mass * abs(self.velocity)**2
        
    def update(self, dt, gravity):
        self.position += self.velocity * dt
        self.velocity += gravity(self.position)*dt
        
    def is_colliding_with(self, other):
        dist = self.position.distance(other.position)
        return dist - self.radius - other.radius <= 0
        
    def collide_with_particle(self, other):
        if self.is_colliding_with(other):
            m1, m2 = self.mass, other.mass
            v1, v2 = self.velocity, other.velocity
            mixer.music.set_volume(abs(v1+v2)/5000)
            mixer.music.play()
            self.velocity = ((m1-m2)*v1 + 2*m2*v2)/(m1+m2)
            other.velocity = ((m2-m1)*v2 + 2*m1*v1)/(m2+m1)
            
            n = (self.position - other.position).direction()
            overlap = self.radius + other.radius - self.position.distance(other.position)
            if overlap == 0:
                return False
            correction = 0.5*n*(overlap+DP*overlap/abs(overlap))
            self.position += correction
            other.position -= correction
            return True
        return False
            
    def check_collision(self, particles, walls):
         changed = True
         while changed:
                 changed = False
                 for wall in walls:
                     if wall.collide_with_particle(self):
                         changed = True
                 for particle in particles:
                     if self == particle:
                         continue
                     if self.collide_with_particle(particle):
                         changed = True
                 
    def __str__(self):
            return "pos : " + str(self.position) + "  \tvel: " + str(self.velocity)
              
    def update_trails(self):
        self.trail.insert (0, (int(self.position.x), int(self.position.y)))
        self.trail.pop(-1)
                 
    def draw(self, screen, color):
        for i in range(len(self.trail)):
            pygame.draw.circle(screen, (0,50,0), self.trail[i],  int(self.radius * (len(self.trail)-1)/len(self.trail)))

        if self.color:
            color = self.color
        pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), self.radius)
    
