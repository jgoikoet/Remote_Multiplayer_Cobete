import asyncio
import math

class colision:

	def __init__(self, p1, p2):

		self.mapOn = None
		self.rectangle = []
		self.rectangles = []
		self.player1 = p1
		self.player2 = p2
	
	async def setList(self):
		self.rectangles = []
		for clave, valor in self.mapOn.items():
			if clave != 'type':
				rectangle = [None] * 4
				rectangle[0] = valor[0]
				rectangle[1] = valor[1]
				rectangle[2] = valor[2]
				rectangle[3] = valor[3]
				self.rectangles.append(rectangle)

	async def checkColision(self):
		for rec in self.rectangles: 
			if (self.player1.move == True and
			self.player1.cobet.x -13 < rec[0] + rec[2] and
			self.player1.cobet.x + 13 > rec[0] and
			self.player1.cobet.y -18 < rec[1] + rec[3] and
			self.player1.cobet.y + 20 > rec[1]):
				self.player1.cobet.speedX = 0
				self.player1.cobet.speedY = 0
				self.player1.cobet.angle = 0
				self.player1.move = False
				task = asyncio.create_task(self.crashWait(self.player1))
	
			if (self.player2.move == True and
			self.player2.cobet.x -13 < rec[0] + rec[2] and
			self.player2.cobet.x + 13 > rec[0] and
			self.player2.cobet.y -18 < rec[1] + rec[3] and
			self.player2.cobet.y + 20 > rec[1]):
				self.player2.cobet.speedX = 0
				self.player2.cobet.speedY = 0
				self.player2.cobet.angle = 0
				self.player2.move = False
				task = asyncio.create_task(self.crashWait(self.player2))

			if (self.player1.cobet.weapon and 
			self.player1.cobet.weaponX < rec[0] + rec[2] and
			self.player1.cobet.weaponX + 4 > rec[0] and
			self.player1.cobet.weaponY < rec[1] + rec[3] and
			self.player1.cobet.weaponY + 4 > rec[1]):
				self.player1.cobet.weapon = False
				self.player1.fire = False
				self.player1.cobet.weaponX = 0
				self.player1.cobet.weaponY = 0

			if (self.player2.cobet.weapon and 
			self.player2.cobet.weaponX < rec[0] + rec[2] and
			self.player2.cobet.weaponX + 4 > rec[0] and
			self.player2.cobet.weaponY < rec[1] + rec[3] and
			self.player2.cobet.weaponY + 4 > rec[1]):
				self.player2.cobet.weapon = False
				self.player2.fire = False
				self.player2.cobet.weaponX = 0
				self.player2.cobet.weaponY = 0

		if (self.player1.cobet.weapon and
			(self.player1.cobet.weaponX < 0 or
			self.player1.cobet.weaponX > 700 or 
			self.player1.cobet.weaponY < 0 or
			self.player1.cobet.weaponY > 600)):
			self.player1.cobet.weapon = False
			self.player1.fire = False
			self.player1.cobet.weaponX = 0
			self.player1.cobet.weaponY = 0

		if (self.player2.cobet.weapon and 
			(self.player2.cobet.weaponX < 0 or
			self.player2.cobet.weaponX > 700 or 
			self.player2.cobet.weaponY < 0 or
			self.player2.cobet.weaponY > 600)):
			self.player2.cobet.weapon = False
			self.player2.fire = False
			self.player2.cobet.weaponX = 0
			self.player2.cobet.weaponY = 0

		if (self.player1.cobet.weapon and self.player2.move == True and 
			self.player2.cobet.x -13 < self.player1.cobet.weaponX + 4 and
			self.player2.cobet.x + 13 > self.player1.cobet.weaponX and
			self.player2.cobet.y -18 < self.player1.cobet.weaponY + 4 and
			self.player2.cobet.y + 20 > self.player1.cobet.weaponY):
			self.player2.cobet.speedX = 0
			self.player2.cobet.speedY = 0
			self.player2.cobet.angle = 0
			self.player2.move = False
			task = asyncio.create_task(self.crashWait(self.player2))
			self.player1.cobet.weapon = False
			self.player1.fire = False
			self.player1.cobet.weaponX = 0
			self.player1.cobet.weaponY = 0

		if (self.player2.cobet.weapon and self.player1.move == True and 
			self.player1.cobet.x -13 < self.player2.cobet.weaponX + 4 and
			self.player1.cobet.x + 13 > self.player2.cobet.weaponX and
			self.player1.cobet.y -18 < self.player2.cobet.weaponY + 4 and
			self.player1.cobet.y + 20 > self.player2.cobet.weaponY):
			self.player1.cobet.speedX = 0
			self.player1.cobet.speedY = 0
			self.player1.cobet.angle = 0
			self.player1.move = False
			task = asyncio.create_task(self.crashWait(self.player1))
			self.player2.cobet.weapon = False
			self.player2.fire = False
			self.player2.cobet.weaponX = 0
			self.player2.cobet.weaponY = 0

		
			
		if (self.player1.move == True and 
		(self.player1.cobet.x -13 < 0 or
		self.player1.cobet.x + 13 > 700 or
		self.player1.cobet.y -18 < 0 or
		self.player1.cobet.y +20 > 600)):
			self.player1.cobet.speedX = 0
			self.player1.cobet.speedY = 0
			self.player1.cobet.angle = 0
			self.player1.move = False
			task = asyncio.create_task(self.crashWait(self.player1))
		
		if (self.player2.move == True and 
		(self.player2.cobet.x -13 < 0 or
		self.player2.cobet.x + 13 > 700 or
		self.player2.cobet.y -18 < 0 or
		self.player2.cobet.y +20 > 600)):
			self.player2.cobet.speedX = 0
			self.player2.cobet.speedY = 0
			self.player2.cobet.angle = 0
			self.player2.move = False
			task = asyncio.create_task(self.crashWait(self.player2))


		if (self.player1.move == True and 
		self.player1.cobet.x -13 > 379 and
		self.player1.cobet.x -13 < 424 and
		self.player1.cobet.y - 18 > 552 and
		(math.sin(math.radians(self.player1.cobet.angle))) > -0.15 and
		(math.sin(math.radians(self.player1.cobet.angle))) < 0.15 and
		(math.cos(math.radians(self.player1.cobet.angle))) > 0):
			self.player1.win = True

		if (self.player2.move == True and
		self.player2.cobet.x -13 > 249 and
		self.player2.cobet.x -13 < 294 and
		self.player2.cobet.y - 18 > 552 and
		(math.sin(math.radians(self.player2.cobet.angle))) > -0.15 and
		(math.sin(math.radians(self.player2.cobet.angle))) < 0.15 and
		(math.cos(math.radians(self.player2.cobet.angle))) > 0):
			self.player2.win = True

	async def crashWait(self, player):
		await asyncio.sleep(3)
		player.move = True
		player.cobet.y = 570
		if player.cobet.color == 'red':
			player.cobet.x = 40
		else:
			player.cobet.x = 660