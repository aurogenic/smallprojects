import sys, os
andr = None
try:
    import android
    andr = True
except ImportError:
    andr = False
try:
    
    
    
    import pygame
    import sys
    import pygame
    import random
    import time
    from pygame.locals import *
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ORANGE = (255, 165, 0)
    BLUE = (0, 64, 128)
    RED = (255, 0, 0)
    fps = 30
    G = 1.20
    JV= -16.0
    
    pygame.init()
     
    screen = pygame.display.set_mode((640, 360) , FULLSCREEN if andr else 0)
    
    font = pygame.font.SysFont("comingsoon", 50, True, True)
    smallfont = pygame.font.SysFont('comingsoon', 20, True)
    mediumfont = pygame.font.SysFont('comingsoon', 35, True, True)
        
    width , height = pygame.display.get_surface().get_size() 
    border= pygame.Rect(0, 0, width, 360)
  
    def loadImg(name, factor = 1):
        img =  pygame.image.load("assets/" + name + ".png")
        img.set_colorkey(BLUE)
        w = img.get_width() * factor
        h = img.get_height() * factor
        return pygame.transform.scale(img, (w, h))
        
    
    title = font.render("Naruto-Dash", 1, ORANGE)
    starttxt = mediumfont.render("tap to start", 1, RED)
    retrytxt = mediumfont.render("tap to retry", 1, RED)
    evbar = pygame.Rect(width-215, 15, 200+ 6, 15)
    
    bg = loadImg("bg", width/736)
    path = loadImg("path", width/2561)
    s1 = loadImg("s1")
    j1 = loadImg("j1")
    r1 = loadImg("r1")
    r2 = loadImg("r2")
    r3 = loadImg("r3")
    r4 = loadImg("r4")
    r5 = loadImg("r5")
    r6 = loadImg("r6")
    d1 = loadImg("d1")
    d2 = loadImg("d2")
    d3 = loadImg("d3")
    e1 = loadImg("e1")
    e2 = loadImg("e2")
    e3 = loadImg("e3")
    
    frogs = []
    for i in range(0, 7):
        frogs.append(loadImg("g" + str(i), 1.5))
    runframes = [r1, r2, r3, r4, r5, r6]
    deathframes = [d1, d2, d3, d3]
    
    state = 0
    frame = s1
    rf = ef = df = 0
    score = 0
   
    ch = r3.get_height()
    x, y = X, Y = (150, height-80)
    basedx = width / fps /3
    dx = dy = 0
    
    p0 = 0
    p1 = width
    wait = 0
    evasion = 50
    
    obstacles = []
    
    def getHS():
        try:
            return int(open("hs.txt", 'r').read())
        except:
            open("hs.txt", 'w').write("0")
        return 0
    def setHS(hs):
        open("hs.txt", 'w').write(str(hs))
    hs = getHS()
    
    def show(img):
        xnew = x - img.get_width()
        ynew = y
        if img in [d2, d3]:
            xnew -= 30
            ynew += 120
        screen.blit(img, (xnew, ynew))
    
    def start():
        global state, score, df, rf, x, y, dx, evasion
        obstacles.clear()
        y = Y
        x = X
        dx = basedx
        df = 0
        rf = 0
        ef = 0
        evasion = 0
        state = 1
        score = 0
    
    def update():
        global y, dy, G, Y, state, score, wait, p0, p1, evasion, dx, hs
        if state == 0:
            screen.blit(starttxt, (width/2 - starttxt.get_width()/2, height- 150))
            dy = 0
            return

        if state == 3:
            screen.blit(retrytxt, (width/2 - retrytxt.get_width()/2, height -150 ))
            for ob in obstacles:
                screen.blit(ob.img, (ob.x, ob.y))
            dy = 0
            return
    	    
        p0 -= dx
        p1 -= dx
        if p1 <= 0:
            p0 = 0
            p1 = width
    	    
        score += 1
        if score > hs:
            hs = score
        if score % 50 ==0:
            dx *= 1.05
        y += dy
        dy += G
        if y >= Y:
            if state == 2:
                state = 1
            y = Y
            dy = 0
    		
        evasion += 1 if evasion < 100 else 0
        wait = wait - dx/3 if wait > 0 else 0
        if wait ==  0:
            r = random.random()
            if r < 0.1:
                obstacles.append(Frog())
        passed = False
        for obstacle in obstacles:
            if (not obstacle.update()):
                passed = True
        if passed:
            obstacles.pop(0)
        collide()
    
    def jump():
        global dy, state, JV
        state = 2
        dy = JV
        
    def death():
        global y, state, x, hs, score
        setHS(hs)
        state = 3
        x = X 
        y = Y 
    	
    	
    def getr():
        global rf
        rf = rf + 1 if 0 <= rf < 12 else 1
        return runframes[int(rf/2)-1]
        
    def gete():
        global ef, state, dx
        ef = ef + 2
        if ef < 5:
            return e1
        if ef  < 25:
            return e2
        if ef > 29:
            unevade()
        return e3
        
    def getd():
        global df
        if df < 9:
            df = df + 1
        return deathframes[int(df/3)]
        
    def getframe():
        if state == 0:
            return s1
        elif state ==1:
            return getr()
        elif state == 2:
            return j1
        elif state == 3:
            return getd()
        else:
            return gete()
            
    def collide():
        global state
        prect = frame.get_rect(x=x-frame.get_width(), y=y).inflate(-80, -80)
        for obstacle in obstacles:
            orect = obstacle.img.get_rect(x = obstacle.x, y = obstacle.y)
            if prect.colliderect(orect):
                if state in [1, 2]:
                    if evasion >= 100:
                        evade()
                        return
                    else:
                        death()
                        
    def evade():
            global evasion, state, dx
            evasion = 0
            dx *= 2
            state = 4
                
    def unevade():
            global ef, dx, state
            ef = 0
            dx /= 2
            state = 1
        
    class Frog:
        def __init__(self):
            global wait
            self.img = random.choice(frogs)
            self.y = Y - self.img.get_height() + ch + 15
            self.x = width
            wait = self.img.get_width()
        
        def update(self):
            self.x -= dx
            if (self.x > - self.img.get_width()):
                screen.blit(self.img, (self.x, self.y))
                return True
            return False
        
    while(True):
        t0 = time.time() 
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, border)
        screen.blit(bg, border)
        screen.blit(path, (p0, Y-50))
        screen.blit(path, (p1, Y-50))
        ievbar = pygame.Rect(width-212, 16, evasion / .5, 13)
        pygame.draw.rect(screen, "#CAF4FF", evbar, border_radius = 6)
        pygame.draw.rect(screen, "#5AB2FF", ievbar, border_radius = 3)
        screen.blit(title, (7, 5))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            

            if event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if state in [0, 3]:
                        start()
                    elif state == 1:
                        jump()
                    elif state == 4:
                        unevade()
                        jump()
        update()
    	
        scoretxt = smallfont.render("score: "+ str(score), 1, BLACK)
        hstxt = smallfont.render("highest: "+ str(hs), 1, BLACK)
        screen.blit(scoretxt, (520, 34))
        screen.blit(hstxt, (425, 34))
        frame = getframe()
    	
        show(frame)
                    
        pygame.display.flip()
        dt =time.time() - t0
        if dt < 1.0/fps:
            pygame.time.wait(int((1.0/fps - dt) * 1000))
    	
   
except Exception as e:
    open('error.txt', 'w').write(str(e))
    raise e