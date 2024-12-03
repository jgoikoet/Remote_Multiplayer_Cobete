import json
import asyncio
import aiohttp
from django.db.models import Q
from asgiref.sync import sync_to_async
from ..models import Match
import logging

from .gamePlayer import gamePlayer

logger = logging.getLogger(__name__)

class gameSetter:

    def __init__(self):
        self.waiting_players = []
        self.connected_players = []
        self.active_rooms= {} 
        self.active_games = {}
        self.tasks = {}


    async def addPlayer(self, player):
        
        logger.info(F"--------{player.display_name} {player.id} ENTRA EN addPlayer--------")

        for roomID in self.active_rooms:
            logger.info(f"al entrar en addPlayer roomID: {roomID}")

        if player.id in self.connected_players:
            self.connected_players.append(player.id)
            await player.connect.send(text_data=json.dumps({
                'type': 'waiting',
                'action': 'duplicated',
            }))
            return

        for p in self.waiting_players:
            logger.info(f"waiting players pre-append ID: {p.id}")

        self.connected_players.append(player.id)
        self.waiting_players.append(player)

        individual_matches = await sync_to_async(Match.objects.filter)(
            Q(player1_id=player.id) | Q(player2_id=player.id))
        individual_played = await sync_to_async(individual_matches.count)()
        individual_won = await sync_to_async(individual_matches.filter(winner_id=player.id).count)()
        win_percentage = (individual_won / individual_played) * 100 if individual_played > 0 else 0

        for p in self.waiting_players:
            logger.info(f"waiting players post-append ID: {p.id}")

        await player.connect.send(text_data=json.dumps({
            'type': 'waiting',
            'action': 'waitForPlayer',
            'name': player.display_name,
            'played': individual_played,            
            'won': individual_won
        }))
        if len(self.waiting_players) >= 2:
            logger.info("-----hay 2 o mas jugadores-------")
            for p in self.waiting_players:
                if p == player:
                    continue

                p_matches = await sync_to_async(Match.objects.filter)(
                    Q(player1_id=p.id) | Q(player2_id=p.id))
                p_played = await sync_to_async(p_matches.count)()
                p_won = await sync_to_async(p_matches.filter(winner_id=p.id).count)()
                p_win_percentage = (p_won / p_played) * 100 if p_played > 0 else 0
                if p_played < 5 or individual_played < 5 or abs(p_win_percentage - win_percentage) <= 25:
                    self.waiting_players.remove(p)
                    self.waiting_players.remove(player)
                    room_id = f"room_{player.id}_{p.id}"
                    player.room_id = room_id
                    p.room_id = room_id
                    game = gamePlayer(player, p)
                    self.active_rooms[room_id] = [player, p]
                    self.active_games[room_id] = game
                    await self.sendWaitingMessage(player, p)
                    task = asyncio.create_task(game.play())
                    self.tasks[room_id] = task
                    break

    async def sendWaitingMessage(self, player1, player2):

        logger.info(f"sendWaitingMessage----player1: {player1.display_name} {player1.id} player2: {player2.display_name} {player2.id}")

        await player1.connect.send(text_data=json.dumps({
            'type': 'waiting',
            'action': 'red',
            'player1Name': player1.display_name,
            'player2Name': player2.display_name
        }))
        await player2.connect.send(text_data=json.dumps({
            'type': 'waiting',
            'action': 'blue',
            'player1Name': player1.display_name,
            'player2Name': player2.display_name
        }))

    
    async def disconnectPlayer(self, player):

        logger.info("---PASO POR AQUI-------")


        if player.id in self.connected_players:
            logger.info(F"SE DESCONECTA {player.display_name} {player.id}")
            self.connected_players.remove(player.id)

        for roomID in self.active_rooms:
            logger.info(f"al entrar e disconectPlayer roomID: {roomID}")

        try:

            if player in self.waiting_players:
                self.waiting_players.remove(player)
                
            if player.room_id in self.active_rooms:
                room = self.active_rooms[player.room_id]
                self.active_rooms.pop(player.room_id, None)
                #active_rooms.pop(player.room_id)
                logger.info(f"desconectado: {player.display_name}, ID: {player.id}")
                self.tasks[player.room_id].cancel()
                if room[0] ==  player:
                    room[1].connect.start = False
                    if room[1].id in self.connected_players:
                        self.connected_players.remove(room[1].id)
                    room[1].resetPlayer()
                    await room[1].connect.send(text_data=json.dumps({
                        'type': 'waiting',
                        'action': 'otherPlayerDisconnect'
                    }))
                    await asyncio.sleep(3)
                    if not room[1].continueGame:
                        await room[1].connect.send(text_data=json.dumps({
                            'type': 'waiting',
                            'action': 'waitForPlayer'
                        }))
                    await self.addPlayer(room[1])
                else:
                    room[0].connect.start = False
                    if room[0].id in self.connected_players:
                        self.connected_players.remove(room[0].id)
                    room[0].resetPlayer()
                    await room[0].connect.send(text_data=json.dumps({
                        'type': 'waiting',
                        'action': 'otherPlayerDisconnect'
                    }))
                    await asyncio.sleep(3)
                    if not room[0].continueGame:
                        await room[0].connect.send(text_data=json.dumps({
                            'type': 'waiting',
                            'action': 'waitForPlayer'
                        }))
                    await self.addPlayer(room[0])
                # if player.room_id in self.active_rooms:
                #     logger.info("-------------BORRAMOS ROOM----------------")
                #     self.active_rooms.pop(player.room_id, None)

            logger.info("---PASO POR AQUI ENDESPUE-------")

        except Exception as e:
            logger.error(f"Error en disconnectPlayer: {e}")