
from .cobete import cobete

class players:

    def __init__(self, connection, id_mumber, display_name):
        self.connect = connection
        self.id = id_mumber
        self.display_name = display_name
        self.cobet = cobete()
        self.room_id = 0
        self.points = 0
        self.continueGame = False
        
        self.left = False
        self.right = False
        self.motor = False
        self.fire = False
        self.move = True
        self.win = False
    
    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def handleMoveMessage(self, message):
        if message == 'leftOn':
            self.left = True
        elif message =='rightOn':
            self.right = True
        elif message == 'motorOn':
            self.motor = True
        elif message == 'fire' and self.move:
            self.fire = True

        if message == 'leftOff':
            self.left = False
        elif message == 'rightOff':
            self.right = False
        elif message == 'motorOff':
            self.motor = False

    def resetPlayer(self):

        self.left = False
        self.right = False
        self.motor = False
        self.fire = False
        self.move = True
        self.win = False
        self.continueGame = False
        self.points = 0

        self.cobet.y = 570
        self.cobet.angle = 0
        self.cobet.speedX = 0
        self.cobet.speedY = 0
        self.cobet.weapon = False
        self.cobet.weaponX = 0
        self.cobet.weaponY = 0
        self.cobet.weaponSpeedX = 0
        self.cobet.weaponSpeedY = 0
