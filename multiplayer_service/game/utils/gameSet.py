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
        self.active_rooms= {} 
        self.active_games = {}
        self.tasks = {}


    async def addPlayer(self, player):

        self.waiting_players.append(player)
        individual_matches = await sync_to_async(Match.objects.filter)(
            Q(player1_id=player.id) | Q(player2_id=player.id))
        individual_played = await sync_to_async(individual_matches.count)()
        individual_won = await sync_to_async(individual_matches.filter(winner_id=player.id).count)()
        win_percentage = (individual_won / individual_played) * 100 if individual_played > 0 else 0
        for p in self.waiting_players:
            logger.info(f"waiting players antes: {p.id}")
        await player.connect.send(text_data=json.dumps({
            'type': 'waiting',
            'action': 'waitForPlayer',
            'name': player.display_name,
            'played': individual_played,            
            'won': individual_won
        }))
        if len(self.waiting_players) >= 2:
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

        if player in self.waiting_players:
            self.waiting_players.remove(player)
            
        elif player.room_id in self.active_rooms:
            self.tasks[player.room_id].cancel()
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
