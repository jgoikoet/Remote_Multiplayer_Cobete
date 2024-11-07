import json
import asyncio

from .gamePlayer import gamePlayer

class gameSetter:

	def __init__(self):
		self.waiting_players = []
		self.active_rooms= {} 
		self.active_games = {} # no se si lo voy a usar
		self.tasks = {}


	async def addPlayer(self, player):

		self.waiting_players.append(player)

		for p in self.waiting_players:
			print("waiting players antes:", p.id)

		await player.connect.send(text_data=json.dumps({
			'type': 'waiting',
			'action': 'waitForPlayer'
		}))


		if len(self.waiting_players) >= 2:
			#self.sendWaitingMessage(player)
			player1 = self.waiting_players.pop(0)
			player2 = self.waiting_players.pop(0)
			room_id = f"room_{player1.id}_{player2.id}"
			player1.room_id = room_id
			player2.room_id = room_id
			game = gamePlayer(player1, player2)
			self.active_rooms[room_id] = [player1, player2]
			self.active_games[room_id] = game

			await self.sendWaitingMessage(player1, player2)
	
			task = asyncio.create_task(game.play())

			self.tasks[room_id] = task

		for p in self.waiting_players:
			print("waiting players endespues:", p.id)
		for r in self.active_rooms.keys():
			print("active room id: ", r)
		for r in self.active_rooms.values():
			print("players in active room:", r[0].id, "  ", r[1].id)

	async def sendWaitingMessage(self, player1, player2):
		print ("Sending messages to players", player1.id, "  ", player2.id)


		await player1.connect.send(text_data=json.dumps({
			'type': 'waiting',
			'action': 'red'
		}))
		await player2.connect.send(text_data=json.dumps({
			'type': 'waiting',
			'action': 'blue'
		}))

	
	async def disconnectPlayer(self, player):

		if player in self.waiting_players:
			self.waiting_players.remove(player)
			print("el desconectado estaba esperando: ", player.id)
			
		elif player.room_id in self.active_rooms:

			self.tasks[player.room_id].cancel()

			print("Active rooms:", self.active_rooms)

			if self.active_rooms[player.room_id][0] ==  player:

				self.active_rooms[player.room_id][1].connect.start = False

				await self.addPlayer(self.active_rooms[player.room_id][1])

				self.active_rooms[player.room_id][1].resetPlayer()

				await self.active_rooms[player.room_id][1].connect.send(text_data=json.dumps({
					'type': 'waiting',
					'action': 'otherPlayerDisconnect'
				}))
				await asyncio.sleep(3)
				await self.active_rooms[player.room_id][1].connect.send(text_data=json.dumps({
					'type': 'waiting',
					'action': 'waitForPlayer'
				}))
			else:

				self.active_rooms[player.room_id][0].connect.start = False

				await self.addPlayer(self.active_rooms[player.room_id][0])

				self.active_rooms[player.room_id][0].resetPlayer()

				await self.active_rooms[player.room_id][0].connect.send(text_data=json.dumps({
					'type': 'waiting',
					'action': 'otherPlayerDisconnect'
				}))
				await asyncio.sleep(3)
				await self.active_rooms[player.room_id][0].connect.send(text_data=json.dumps({
					'type': 'waiting',
					'action': 'waitForPlayer'
				}))

			self.active_rooms.pop(player.room_id, None)
			#self.active_games.pop(player.room_id, None) # NO SE SI ES NECESARIO...
			print("-- Active rooms:", self.active_rooms)
			print("-- Active waiters", self.waiting_players)