import json

map1 = {
	'type': 'map',
	'r1': [345, 170, 10, 430, 'lime'],
	'r2': [100, 75, 190, 10, 'orange'],
	'r3': [410, 75, 190, 10, 'orange'],
	'r4': [25, 200, 200, 10, 'orange'],
	'r5': [475, 200, 200, 10, 'orange'],
	'r6': [175, 350, 10, 250, 'orange'],
	'r7': [525, 350, 10, 250, 'orange']
}

map2 = {
	'type': 'map',
	'r1': [250, 200, 200, 30, 'purple'],
	'r2': [345, 150, 10, 450, 'lime'],
	'r3': [100, 70, 120, 30, 'yellow'],
	'r4': [480, 70, 120, 30, 'yellow'],
	'r5': [50, 200, 30, 30, 'purple'],
	'r6': [620, 200, 30, 30, 'purple'],
	'r7': [150, 200, 30, 30, 'purple'],
	'r8': [520, 200, 30, 30, 'purple'],
	'r9': [50, 300, 30, 30, 'purple'],
	'r10': [620, 300, 30, 30, 'purple'],
	'r11': [150, 300, 30, 30, 'purple'],
	'r12': [520, 300, 30, 30, 'purple'],
	'r13': [250, 300, 30, 30, 'purple'],
	'r14': [420, 300, 30, 30, 'purple'],
	'r15': [175, 400, 10, 200, 'orange'],
	'r16': [525, 400, 10, 200, 'orange'],
}

map3 = {
	'type': 'map',
	'r1': [345, 280, 10, 320, 'lime'],
	'r2': [150, 85, 30, 30, 'purple'],
	'r3': [520, 85, 30, 30, 'purple'],
	'r4': [250, 85, 30, 30, 'purple'],
	'r5': [420, 85, 30, 30, 'purple'],
	'r6': [100, 300, 10, 300, 'lime'],
	'r7': [590, 300, 10, 300, 'lime'],
	'r8': [280, 210, 10, 100, 'lime'],
	'r9': [410, 210, 10, 100, 'lime'],
	'r10': [100, 200, 500, 10, 'orange']
}

async def map1Send(player1, player2):
	await player1.connect.send(text_data=json.dumps(map1))
	await player2.connect.send(text_data=json.dumps(map1))

async def map2Send(player1, player2):
	await player1.connect.send(text_data=json.dumps(map2))
	await player2.connect.send(text_data=json.dumps(map2))

async def map3Send(player1, player2):
	await player1.connect.send(text_data=json.dumps(map3))
	await player2.connect.send(text_data=json.dumps(map3))