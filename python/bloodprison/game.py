from PIL import Image, ImageDraw, ImageFont
import random
import os

class Tournament:
	def __init__(self, players, rounds=10, reMatches = 2, allowSelf=True):
		self.players = players
		self.rounds = rounds
		self.reMatches = reMatches
		self.allowSelf= allowSelf
	
	
	def start(self):
		n = 1
		points = {}
		folder = input("enter new folder name store results: ")
		dir = os.getcwd() 
		path = os.path.join(dir, folder)
		try:
			os.mkdir(path)
		except:
			print("folder already exists")
			
		texth = 48
		
		n = len(self.players)
		if self.allowSelf:
			n += 1
		h = (texth+2)*(n*n + 3 )
		wd = 640
			
		bg = (50, 50, 50)
		w = (250, 250, 250)
		table = Image.new('RGB', (wd, h), 'black')
		drawtable = ImageDraw.Draw(table)
		font = ImageFont.load_default().font_variant(size=texth)
		line = 0
		
		for player in self.players:
			points[player] = 0
		for i in range(int(self.reMatches/2)):
			for p1 in self.players:
				for p2 in self.players:
					if self.allowSelf or p1 is not p2:
						game = Game(p1, p2, self.rounds, folder)
						game.start()
						game.saveImg(f"{p1.name}vs{p2.name}.png")
						print("\nmatch", n)
						n += 1
						print(p1.name, game.p1score)
						print(p2.name, game.p2score)
						points[p1] += game.p1score
						points[p2] += game.p2score
						(n1, n2) = game.result()
						drawtable.text((texth, line*(texth+2)), f"{p1}", font=font, fill='white')
						drawtable.text((wd/2 - texth*1.5, line*(texth+2)), f"{n1}  -  {n2}", font=font, fill='white')
						drawtable.text((wd/2+3*texth, line*(texth+2)), f"{p2}", font=font, fill='white')
						line += 1
		line += 2
					 	
		print("\n\nscores")
		for player in self.players:
			print(player.name, points[player])
			drawtable.text((texth, line*(texth+2)), f"{player} - {points[player]}", font=font, fill='white')
			line += 1
			
		if folder != "":
		 	table.save(folder+"/results.png")
		else:
		 	table.save('results.png')
		print("images generated")
				
								
class Game:
    def __init__(self, p1, p2, rounds=10, folder=""):
        self.p1 = p1
        self.p2 = p2
        self.rounds = rounds
        self.p1score = 0
        self.p2score = 0
        self.p1Choices =  []
        self.p2Choices = []
        self.folder = folder
        if self.folder != "":
        	self.folder = folder + "/"
        
    def start(self):
        for i in range(self.rounds):
            self.p1Choice = self.p1.choose()
            self.p1Choices.append(self.p1Choice)
            self.p2Choice = self.p2.choose()
            self.p2Choices.append(self.p2Choice)
            self.evaluate()
        self.p1.reset()
        self.p2.reset()
    
    def evaluate(self):
        if self.p1Choice:
            if self.p2Choice:
                self.addScore(3, 3)
            else:
                self.addScore(0, 5)
        elif self.p2Choice:
            self.addScore(5, 0)
        else:
            self.addScore(1, 1)

    def addScore(self, x, y):
        self.p1score += x
        self.p2score += y
        self.p1.upt(x, y)
        self.p2.upt(y, x)
            
    def result(self):
      	  return (self.p1score, self.p2score)
      	  
    def saveImg(self, p=None):
    	w = 50
    	b = 5
    	bg = (50, 50, 50)
    	s = (120, 120, 255)
    	f = (255, 0, 0)
    	img = Image.new('RGB',((self.rounds+1)*(w+b)+b, 3*w+3*b) , color=bg)
    	draw = ImageDraw.Draw(img)
    	font = ImageFont.load_default().font_variant(size=w-10)
    	draw.text((b, b), f"{self.p1.name} vs {self.p2.name}", font=font, fill='white')
    	
    	for i, val in enumerate(self.p1Choices):
    		color = s if val else f
    		for x in range(i*(w+b)+b, (i+1)*(w+b)):
    			for y in range(w+b, w+b+w):
    				img.putpixel((x, y), color)
    	draw.text((self.rounds*(w+b)+b, w+b+5), str(self.p1score), font=font, fill="white")
    			
    	for i, val in enumerate(self.p2Choices):
    		color = s if val else f
    		for x in range(i*(w+b)+b, (i+1)*(w+b)):
    			for y in range(w+b+w+b, w+b+w+b+w):
    				img.putpixel((x, y),  color)
    	draw.text((self.rounds*(w+b)+b, w+b+w+b+5), str(self.p2score), font=font, fill="white")
    	
    	if p is not None:
    		img.save(self.folder+p)
    	return img
        	
class Player:
	def __init__(self, name='anonymous'):
		self.name = name
		self.myScore = 0
		self.opScore = 0
		
	def __str__(self):
		return self.name
	
	def choose(self):
		return True
		
	def upt(self, x, y):
		self.myScore += x
		self.opScore += y

	def reset(self):
		self.myScore = 0
		self.opScore = 0
		
class TitForTatPlayer(Player):
	def __init__(self, name='ANMS'):
		super().__init__(name)
		self.lastScore = 3
		
	def choose(self):
		return self.lastScore > 2
			
	def upt(self, x , y):
		super().upt(x, y)
		self.lastScore = x
		
	def reset(self):
		super().reset()
		self.lastScore = 3
		
class GreedyPlayer(Player):
	def choose(self):
		return False

class RandomPlayer(Player):
	def choose(self):
		return random.choice((True, False))
		
	
p1 = TitForTatPlayer('T4T')
p2 = RandomPlayer('RNDM')
p3 = GreedyPlayer('Greedy')
players = [p1, p2, p3]
tournament = Tournament(players,)
tournament.start()
