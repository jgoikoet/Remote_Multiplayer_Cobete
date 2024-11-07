
class cobete:

    def __init__(self):
        self.x = 0
        self.y = 570
        self.color = 'none'
        self.angle = 0
        self.speedX = 0
        self.speedY = 0

        self.weapon = False
        self.weaponX = 0
        self.weaponY = 0
        self.weaponTotalSpeed = 8
        self.weaponSpeedX = 0
        self.weaponSpeedY = 0

    def setPosition(self, pX):
        self.x = pX
