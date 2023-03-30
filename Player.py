from graphics import *
from Rendering import *
from Utility import clamp

class Player:
    health = 3
    x, y = 0, 0
    spriteDir = "TestSprite1"

    def __init__(self, tMap, win):
        self.map = tMap
        self.sprite = Sprite(self.spriteDir, tMap.tileToPoint(self.x, self.y), win)

    def move(self, x, y):
        self.x = clamp(self.x + x, 0, self.map.width - 1)
        self.y = clamp(self.y + y, 0, self.map.height - 1)
        p = self.map.tileToPoint(self.x, self.y)
        self.sprite.move(Point(p.x - self.sprite.position.x, p.y - self.sprite.position.y))