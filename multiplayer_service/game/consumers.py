import json
import jwt
import logging  
from django.conf import settings

logger = logging.getLogger(__name__) 

from channels.generic.websocket import AsyncWebsocketConsumer

from .utils.player import players
from .utils.gameSet import gameSetter

# Diccionario global para mantener a los jugadores esperando
waiting_players = []

id = 1

gameSet = gameSetter()

class GameMatchmakingConsumer(AsyncWebsocketConsumer):
	def decode_jwt_token(self, token):
		try:
			# Decodifica el token usando la clave secreta de Django
			payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
			return payload
		except Exception as e:
			print(f"Error decodificando token: {str(e)}")
			return None

	async def connect(self):
		"""Cuando un cliente se conecta al WebSocket."""
		print("se ha conectado un cliente")
		await self.accept()  # Acepta la conexión del WebSocket
		self.player = None

	async def disconnect(self, close_code):
		"""Cuando el cliente se desconecta."""
		print("Entrada en desconexion")
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
			id =  await self.handle_action_join_game(data)
			display_name =  await self.handle_action_join_game_display_name(data)			
			logger.info(f"display_name: {display_name}")
			logger.error(f"User ID: {id}")
			self.player = players(self, id ,display_name)
			print("Ha hecho join", self.player.id)
			id += 1
			await gameSet.addPlayer(self.player)
		elif message_type == 'start':
			self.start = True
		elif message_type == 'continueGame':
			self.player.continueGame = True

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
