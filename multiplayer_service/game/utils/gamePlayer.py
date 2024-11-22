import json
import asyncio
import math
import logging
from asgiref.sync import sync_to_async

from .maps import map1Send, map2Send, map3Send
from .colision import colision
from .maps import map1, map2, map3
from ..models import Match

logger = logging.getLogger(__name__) 


class gamePlayer:
	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2
		self.player1.cobet.setPosition(40)
		self.player2.cobet.setPosition(660)
		self.player1.cobet.color = 'red'
		self.player2.cobet.color = 'blue'
		self.start = False
		self.speedIncrement = 0.05
		self.angleChange = 4
		self.crash = colision(player1, player2)
		self.crash.mapOn = map1
		self.playOn = True
	
		#self.init = True
	

	async def play(self):
		print("AKI PLAY")
		while not self.player1.connect.start or not self.player2.connect.start:
			if self.player1.connect.start == True and self.start == False:
				await self.player1.connect.send(text_data=json.dumps({
				'type': 'waiting',
				'action': 'ready'
				}))
				self.start = True
			if self.player2.connect.start == True and self.start == False:
				await self.player2.connect.send(text_data=json.dumps({
				'type': 'waiting',
				'action': 'ready'
				}))
				self.start = True
			await asyncio.sleep(0.001)
		await map1Send(self.player1, self.player2)
		self.playOn = True
		await self.playing()
				
	async def playing(self):
		await self.crash.setList()
		while(self.playOn):

			if self.player1.left == True and self.player1.move:
				self.player1.cobet.angle -= self.angleChange
			if self.player1.right == True and self.player1.move:
				self.player1.cobet.angle += self.angleChange

			if self.player2.left == True and self.player2.move:
				self.player2.cobet.angle -= self.angleChange
			if self.player2.right == True and self.player2.move:
				self.player2.cobet.angle += self.angleChange
			
			if self.player1.motor == True and self.player1.move:
				self.player1.cobet.speedX += (math.sin(math.radians(self.player1.cobet.angle))) * self.speedIncrement
				self.player1.cobet.speedY += (-math.cos(math.radians(self.player1.cobet.angle))) * self.speedIncrement
			
			if self.player2.motor == True and self.player2.move:
				self.player2.cobet.speedX += (math.sin(math.radians(self.player2.cobet.angle))) * self.speedIncrement
				self.player2.cobet.speedY += (-math.cos(math.radians(self.player2.cobet.angle))) * self.speedIncrement

			if self.player1.fire == True and self.player1.cobet.weapon == False: 
				self.player1.fire = False
				self.player1.cobet.weapon = True
				self.player1.cobet.weaponX = self.player1.cobet.x
				self.player1.cobet.weaponY = self.player1.cobet.y
				self.player1.cobet.weaponSpeedX = (math.sin(math.radians(self.player1.cobet.angle))) * self.player1.cobet.weaponTotalSpeed
				self.player1.cobet.weaponSpeedY = (-math.cos(math.radians(self.player1.cobet.angle))) * self.player1.cobet.weaponTotalSpeed


			if self.player2.fire == True and self.player2.cobet.weapon == False: 
				self.player2.fire = False
				self.player2.cobet.weapon = True
				self.player2.cobet.weaponX = self.player2.cobet.x
				self.player2.cobet.weaponY = self.player2.cobet.y
				self.player2.cobet.weaponSpeedX = (math.sin(math.radians(self.player2.cobet.angle))) * self.player2.cobet.weaponTotalSpeed
				self.player2.cobet.weaponSpeedY = (-math.cos(math.radians(self.player2.cobet.angle))) * self.player2.cobet.weaponTotalSpeed

			if self.player1.cobet.weapon:
				self.player1.cobet.weaponX += self.player1.cobet.weaponSpeedX
				self.player1.cobet.weaponY += self.player1.cobet.weaponSpeedY
			
			if self.player2.cobet.weapon:
				self.player2.cobet.weaponX += self.player2.cobet.weaponSpeedX
				self.player2.cobet.weaponY += self.player2.cobet.weaponSpeedY

			self.player1.cobet.x +=  self.player1.cobet.speedX
			self.player1.cobet.y +=  self.player1.cobet.speedY
			self.player2.cobet.x +=  self.player2.cobet.speedX
			self.player2.cobet.y +=  self.player2.cobet.speedY

			await self.crash.checkColision()
			await self.sendGameState()

			if self.player1.win == True or self.player2.win == True:
				await self.winner()

			await asyncio.sleep(0.010)
			
	async def gameEnd(self):


		if self.player1.points > self.player2.points:
			winner = self.player1.id
		else:
			winner = self.player2.id
		
		data = {
			"player1_id": self.player1.id,
			"player2_id": self.player2.id,
			"player1_display_name": self.player1.display_name,
			"player2_display_name": self.player2.display_name,
			"player1_score": self.player1.points,
			"player2_score": self.player2.points,
			"winner_id": winner
		}
		
		await sync_to_async(Match.objects.create)(**data)

		self.crash.mapOn = map1
		self.player1.connect.start = False
		self.player2.connect.start = False
		self.player1.points = 0
		self.player2.points = 0
		self.playOn = False
		self.start = False
		await self.resetGame()
		await self.play()

	async def winner(self):

		if self.player1.win:
			self.player1.points += 1
		else:
			self.player2.points += 1

		if self.player1.win:
			await self.player1.connect.send(text_data=json.dumps({
				'type': 'waiting',
				'action': 'redPoint1'
			}))
			await self.player2.connect.send(text_data=json.dumps({
				'type': 'waiting',
				'action': 'redPoint1'
			}))
			await asyncio.sleep(1)
			await self.player1.connect.send(text_data=json.dumps({
				'type': 'waiting',
				'action': 'redPoint2'
			}))
			await self.player2.connect.send(text_data=json.dumps({
				'type': 'waiting',
				'action': 'redPoint2'
			}))
			await asyncio.sleep(1)
			if self.player1.points == 2:
				await self.player1.connect.send(text_data=json.dumps({
					'type': 'waiting',
					'action': 'redWinGame'
				}))
				await self.player2.connect.send(text_data=json.dumps({
					'type': 'waiting',
					'action': 'redWinGame'
				}))
				await self.gameEnd()
				return
			else:
				await self.player1.connect.send(text_data=json.dumps({
					'type': 'waiting',
					'action': 'redPoint3'
				}))
				await self.player2.connect.send(text_data=json.dumps({
					'type': 'waiting',
					'action': 'redPoint3'
				}))
		else:
			await self.player1.connect.send(text_data=json.dumps({
				'type': 'waiting',
				'action': 'bluePoint1'
			}))
			await self.player2.connect.send(text_data=json.dumps({
				'type': 'waiting',
				'action': 'bluePoint1'
			}))
			await asyncio.sleep(1)
			await self.player1.connect.send(text_data=json.dumps({
				'type': 'waiting',
				'action': 'bluePoint2'
			}))
			await self.player2.connect.send(text_data=json.dumps({
				'type': 'waiting',
				'action': 'bluePoint2'
			}))
			await asyncio.sleep(1)
			if self.player2.points == 2:
				await self.player1.connect.send(text_data=json.dumps({
					'type': 'waiting',
					'action': 'blueWinGame'
				}))
				await self.player2.connect.send(text_data=json.dumps({
					'type': 'waiting',
					'action': 'blueWinGame'
				}))
				await self.gameEnd()
				return
			else:
				await self.player1.connect.send(text_data=json.dumps({
					'type': 'waiting',
					'action': 'bluePoint3'
				}))
				await self.player2.connect.send(text_data=json.dumps({
					'type': 'waiting',
					'action': 'bluePoint3'
				}))


		while self.player1.continueGame == False or self.player2.continueGame == False:
			if self.player1.continueGame:
				await self.player1.connect.send(text_data=json.dumps({
				'type': 'waiting',
				'action': 'ready'
			}))
			if self.player2.continueGame:
				await self.player2.connect.send(text_data=json.dumps({
				'type': 'waiting',
				'action': 'ready'
			}))

			await asyncio.sleep(0.001)

		if self.player1.points + self.player2.points == 1:
			self.crash.mapOn = map2
			await map2Send(self.player1, self.player2)
			await self.crash.setList()
		elif self.player1.points == 1 and self.player2.points == 1:
			self.crash.mapOn = map3
			await map3Send(self.player1, self.player2)
			await self.crash.setList()
			
		await self.resetGame()


	async def resetGame(self):
		self.player1.cobet.x = 40
		self.player1.cobet.y = 570
		self.player2.cobet.x = 660
		self.player2.cobet.y = 570
		self.player1.cobet.speedX = 0
		self.player1.cobet.speedY = 0
		self.player2.cobet.speedX = 0
		self.player2.cobet.speedY = 0
		self.player1.cobet.angle = 0
		self.player2.cobet.angle = 0
		self.player1.move = True
		self.player2.move = True
		self.player1.win = False
		self.player2.win = False
		self.player1.continueGame = False
		self.player2.continueGame = False


	async def sendGameState(self):
		await self.player1.connect.send(text_data=json.dumps({
			'type': 'refresh',
			'player1X': self.player1.cobet.x,
			'player1Y': self.player1.cobet.y,
			'player1Display_name': self.player1.display_name,
			'player2Display_name': self.player2.display_name,			
			'player1Angle': self.player1.cobet.angle,
			'player1Motor': self.player1.motor,
			'player1Move': self.player1.move,
			'player2X': self.player2.cobet.x,
			'player2Y': self.player2.cobet.y,
			'player2Angle': self.player2.cobet.angle,
			'player2Motor': self.player2.motor,
			'player2Move': self.player2.move,
			'player1WeaponX': self.player1.cobet.weaponX,
			'player1WeaponY': self.player1.cobet.weaponY,
			'player2WeaponX': self.player2.cobet.weaponX,
			'player2WeaponY': self.player2.cobet.weaponY

		}))
		await self.player2.connect.send(text_data=json.dumps({
			'type': 'refresh',
			'player1Display_name': self.player1.display_name,
			'player2Display_name': self.player2.display_name,				
			'player1X': self.player1.cobet.x,
			'player1Y': self.player1.cobet.y,
			'player1Angle': self.player1.cobet.angle,
			'player1Motor': self.player1.motor,
			'player1Move': self.player1.move,
			'player2X': self.player2.cobet.x,
			'player2Y': self.player2.cobet.y,
			'player2Angle': self.player2.cobet.angle,
			'player2Motor': self.player2.motor,
			'player2Move': self.player2.move,
			'player1WeaponX': self.player1.cobet.weaponX,
			'player1WeaponY': self.player1.cobet.weaponY,
			'player2WeaponX': self.player2.cobet.weaponX,
			'player2WeaponY': self.player2.cobet.weaponY
		}))

