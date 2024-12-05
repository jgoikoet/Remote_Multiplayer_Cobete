import json
import jwt
import logging  
from django.conf import settings
import asyncio

logger = logging.getLogger(__name__) 

from channels.generic.websocket import AsyncWebsocketConsumer

from .utils.player import players
from .utils.gameSet import gameSetter

waiting_players = []

# id = 1

gameSet = gameSetter()

class GameMatchmakingConsumer(AsyncWebsocketConsumer):
	def decode_jwt_token(self, token):
		try:
			payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
			return payload
		except Exception as e:
			return None

	async def connect(self):
		await asyncio.sleep(0.5)
		await self.accept() 
		self.player = None

	async def disconnect(self, close_code):
		# await asyncio.sleep(0.1)
		logger.info(f"-------------------disconnect {self.player.display_name} {self.player.id}")
		await gameSet.disconnectPlayer(self.player)
		# logger.info("------HA VUELTO--------")

	async def receive(self, text_data):
		# global id
		data = json.loads(text_data)
		message_type = data.get('type', 0)
		message_action = data.get('action', 0)
		if message_type == 'move':
			self.player.handleMoveMessage(message_action)
		elif message_type == 'join_game':
			self.start = False
			id =  await self.handle_action_join_game(data)
			display_name =  await self.handle_action_join_game_display_name(data)
			self.player = players(self, id ,display_name)
			# id += 1
			await gameSet.addPlayer(self.player)
		elif message_type == 'start':
			self.start = True
		elif message_type == 'continueGame':
			self.player.continueGame = True

	async def handle_action_join_game(self, data):
		id = 0
		if 'token' not in data:
			return id
		payload = self.decode_jwt_token(data['token'])
		if payload is None:
			return id
		id = payload.get('user_id')
		return id

	async def handle_action_join_game_display_name(self, data):
		display_name = ""
		if 'token' not in data:
			return display_name
		payload = self.decode_jwt_token(data['token'])
		if payload is None:
			return display_name
		display_name = payload.get('display_name', "")
		return display_name
