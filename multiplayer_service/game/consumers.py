import json
import time
import asyncio



#aqui toco
import jwt
import logging  

from django.conf import settings
from datetime import datetime


logger = logging.getLogger(__name__) 

#fin aqui toco

from channels.generic.websocket import AsyncWebsocketConsumer

from .utils.player import players
from .utils.gameSet import gameSetter

# Diccionario global para mantener a los jugadores esperando
waiting_players = []

# Diccionario para almacenar las salas activas (por simplicidad, puede ser reemplazado por una base de datos)
#active_rooms = {}

id = 1

gameSet = gameSetter()



class GameMatchmakingConsumer(AsyncWebsocketConsumer):


	#aqui toco

	def decode_jwt_token(self, token):
		try:
			# Decodifica el token usando la clave secreta de Django
			payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
			return payload
		except Exception as e:
			print(f"Error decodificando token: {str(e)}")
			return None

	#fin aqui toco

	async def connect(self):
		"""Cuando un cliente se conecta al WebSocket."""
		print("se ha conectado un cliente")
		await self.accept()  # Acepta la conexión del WebSocket
		self.player = None

	async def disconnect(self, close_code):
		"""Cuando el cliente se desconecta."""
		print("Entrada en desconexion")
		
		# Si el jugador estaba joineado (independientemente de que este en una partida o no)
		# if (self.player in gameSet.waiting_players or
		# (self.player and self.player.room_id in  gameSet.active_rooms)):
		logger.error(f"Disconected Player: {self.player}")
		await gameSet.disconnectPlayer(self.player)


	async def receive(self, text_data):
		"""Manejar mensajes recibidos de los jugadores."""
		global id

		data = json.loads(text_data)
		message_type = data.get('type', 0)
		message_action = data.get('action', 0)
		if message_type == 'move':
			self.player.handleMoveMessage(message_action)
		elif message_type == 'join_game':
			self.start = False
			logger.error(f"Datos ID: {data}")
	        #aqui toco			
			id =  await self.handle_action_join_game(data)
			display_name =  await self.handle_action_join_game_display_name(data)			
			logger.info(f"display_name: {display_name}")
			logger.error(f"User ID: {id}")
			self.player = players(self, id ,display_name)
			#			self.player = players(self, id)		
            #			await self.handle_action_join_game(data)



			print("Ha hecho join", self.player.id)
			id += 1
			await gameSet.addPlayer(self.player)
		elif message_type == 'start':
			self.start = True
		elif message_type == 'continueGame':
			self.player.continueGame = True
			
		#elif message_type == 'press_space':

		# if message_type == 'join_game':
		# 	await self.handle_action_join_game(data)
		#print(message_action)
		# await self.send(text_data=json.dumps({
		# 	'type': 'prueba',
		# 	'message': message_action
		# }))
		#await pru(data)
		# elif message_type == 'move':
		# 	await self.handle_action_player_movement(data)
		# else:
		# 	await self.send(text_data=json.dumps({
		# 		'type': 'error',
		# 		'message': "Bad request, parameter 'type' is mandatory"
		# 	}))


	async def handle_action_join_game(self, data):
		# Verificar que el token existe
		id = 0
		if 'token' not in data:
			return id

		payload = self.decode_jwt_token(data['token'])
		if payload is None:
			return id
		logger.error(f"Payload: {payload}")
		logger.error(f"Payload User:id: {payload.get('user_id')}")
		id = payload.get('user_id')

		return id
	#fin aqui toco

	async def handle_action_join_game_display_name(self, data):
		# Verificar que el token existe
		display_name = ""
		if 'token' not in data:
			return display_name

		payload = self.decode_jwt_token(data['token'])

		if payload is None:
			return display_name

		logger.error(f"Payload display: {payload}")
		logger.error(f"Payload User:display_name: {payload.get('display_name')}")

		display_name = payload.get('display_name', "")

		return display_name

	#async def handle_action_join_game(self, data):
		# global id
		# print ("ha habido join")
		# player = players(self, id)
		# await player.connect.send(text_data=json.dumps({
		# 	'type': 'prueba',
		# 	'message': 'hola torpedo'
		# }))
		# id += 1
		# waiting_players.append(player)
		# await self.match_players()
		#self.user_id = data.get('user_id', 0)
		# global id
		# print (f"id = {id}")
		# self.user_id = id
		# id += 1
		# if self.user_id:
		# 	waiting_players.append(self)
		# 	await self.match_players()
		# else:
		# 	await self.send(text_data=json.dumps({
		# 		'type': 'error',
		# 		'message': "Bad request, parameter 'user_id' is mandatory"
		# 	}))

	# async def match_players(self):
	# 	"""Intenta emparejar jugadores en la lista de espera."""
		# if len(waiting_players) >= 2:  # Necesitamos al menos dos jugadores para emparejar
		# 	# Emparejar a los dos primeros jugadores
		# 	player1 = waiting_players.pop(0)
		# 	player2 = waiting_players.pop(0)
		# 	await self.init_new_game(player1, player2)
		# 	print ("hay partido")
		# 	await self.notify_match_found(player1, player2)
	# 		#await asyncio.sleep(1)
	# 		asyncio.create_task(self.update_positions(self.room_id))
	# 		await self.notify_start_game(player1, player2)

	# async def init_new_game(self, player1, player2):
	# 	# Crear una nueva sala para la partida
	# 	room_id = f"room_{player1.id}_{player2.id}"

		# active_rooms[room_id] = [player1, player2]
	# 	active_rooms[room_id] = {
	# 		'player1': player1,
	# 		'player2': player2,
	# 		'game_state': {
	# 			'player1X' : 40,
	# 			'player1Y': 570,
	# 			'Player1Points': 0,
	# 			'player1Left': False,
	# 			'player1Right': False,
	# 			'player1SpeedX': 0,
	# 			'player1SpeedY': 0,
	# 			'player1Angle': 0,

	# 			'player2X': 660,
	# 			'player2Y': 570,
	# 			'Player2Points': 0,
	# 			'player2Left': False,
	# 			'player2Right': False,
	# 			'player2SpeedX': 0,
	# 			'player2SpeedY': 0,
	# 			'player2Angle': 0, 
	# 		}
	# 	}
		
	# 	player1.room_id = room_id
	# 	player2.room_id = room_id

	# async def countdown(self, player1, player2):
	# 	await player1.send(text_data=json.dumps({
	# 		'type': 'new_message',
	# 		'messagge': '3',
	# 		'color':  'palegreen'
	# 	}))
	# 	await player2.send(text_data=json.dumps({
	# 		'type': 'new_message',
	# 		'messagge': '3',
	# 		'color':  'palegreen'
	# 	}))
	# 	await asyncio.sleep(1)
	# 	await player1.send(text_data=json.dumps({
	# 		'type': 'new_message',
	# 		'messagge': '2',
	# 		'color':  'palegreen'
	# 	}))
	# 	await player2.send(text_data=json.dumps({
	# 		'type': 'new_message',
	# 		'messagge': '2',
	# 		'color':  'palegreen'
	# 	}))
	# 	await asyncio.sleep(1)
	# 	await player1.send(text_data=json.dumps({
	# 		'type': 'new_message',
	# 		'messagge': '1',
	# 		'color':  'palegreen'
	# 	}))
	# 	await player2.send(text_data=json.dumps({
	# 		'type': 'new_message',
	# 		'messagge': '1',
	# 		'color':  'palegreen'
	# 	}))
	# 	await asyncio.sleep(1)
	# 	await player1.send(text_data=json.dumps({
	# 		'type': 'start_game',
	# 	}))
	# 	await player2.send(text_data=json.dumps({
	# 		'type': 'start_game',
	# 	}))
		

	""" async def notify_match_found(self, player1, player2):
		# Notificar a ambos jugadores que están emparejados y la partida va a empezar
		await player1.connect.send(text_data=json.dumps({
			'type': 'match_found',
			#'room': player1.room_id,
			'messagge': '¡Mach Found!',
			'color':  'palegreen',
			'number': player1.id
		}))
		await player2.connect.send(text_data=json.dumps({
			'type': 'match_found',
			#'room': player2.room_id,
			'messagge': '¡Mach Found!',
			'color':  'palegreen',
			'number': player2.id
		})) """
	# 	await asyncio.sleep(1)
	# 	await self.countdown(player1, player2)

	# async def notify_start_game(self, player1, player2):
	# 	# Iniciar el juego enviando un mensaje de sincronización a ambos jugadores
	# 	await player1.send(text_data=json.dumps({
	# 		'type': 'start_game'
	# 	}))
	# 	await player2.send(text_data=json.dumps({
	# 		'type': 'start_game'
	# 	}))

	# async def handle_action_player_movement(self, data):
	# 	room = active_rooms.get(self.room_id, [])
	# 	movement_direction = data.get('action', 0)
	# 	is_player1 = room['player1'].user_id == self.user_id
	# 	#print(f"amos pulsao tecla {movement_direction}")
		
	# 	if movement_direction == 'upOn':
	# 		if is_player1:
	# 			room['game_state']['player1up'] = True
	# 		else:
	# 			room['game_state']['player2up'] = True

	# async def send_game_state_update(self, room, speedx, speedy):

	# 	await room['player1'].send(text_data=json.dumps({
	# 		'type': 'game_state_update',
	# 		'player1Y': room['game_state']['player1Y'],
	# 		'player2Y': room['game_state']['player2Y'],
	# 		'ballX': room['game_state']['ball']['position']['x'],
	# 		'ballY': room['game_state']['ball']['position']['y'],
	# 		'speedX': speedx,
	# 		'speedY': speedy,
	# 		'time': time.time()
	# 	}))
	# 	await room['player2'].send(text_data=json.dumps({
	# 		'type': 'game_state_update',
	# 		'player1Y': room['game_state']['player1Y'],
	# 		'player2Y': room['game_state']['player2Y'],
	# 		'ballX': room['game_state']['ball']['position']['x'],
	# 		'ballY': room['game_state']['ball']['position']['y'],
	# 		'speedX': speedx,
	# 		'speedY': speedy,
	# 		'time': time.time()
	# 	}))

	# async def update_positions(self, room_id):
	# 	room = active_rooms.get(room_id, [])

	# 	while playing:
			
	# 		await self.send_game_state_update(room, speedX, speedY)
	# 		await asyncio.sleep(0.030)  #  0.030 .002Actualizar la pelota cada x ms


	# async def marker_update(self, room, player):
	# 	if player == 1:
	# 		room['game_state']['Player1Points'] += 1
	# 	else:
	# 		room['game_state']['Player2Points'] += 1

	# 	room['game_state']['ball']['position']['x'] = 300
	# 	room['game_state']['ball']['position']['y'] = 200
		
	# 	room['game_state']['player1Y'] = 150
	# 	room['game_state']['player2Y'] = 150
