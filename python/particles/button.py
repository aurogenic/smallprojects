import pygame

class Button:
    def __init__(self, text, color, x, y, width, height):
        self.text = text
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('comicsans',60)
        if text != "":
            self.textsurf = self.font.render(text, 1, (0,0,0))
    
    def draw(self, screen, outline= None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height +4), 0)
        
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != "":
            screen.blit(self.textsurf, (self.x + (self.width/2 - self.textsurf.get_width()/2), self.y + (self.height/2 - self.textsurf.get_height()/2)))
            
    def ison(self, x, y):
            return   ( self.x < x < self.x + self.width and  self.y < y < self.y + self.height)
            
            
            