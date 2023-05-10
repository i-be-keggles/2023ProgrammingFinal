from Rendering import *
from graphics import *

class Object:
    driver = None

    def __init__(self, name, pos, tMap, win, sprite = None):
        self.name = name
        self.position = Point(pos.x, pos.y)
        self.tMap = tMap
        self.win = win

        if sprite is not None:
            self.sprite = Sprite(sprite, tMap.tileToPoint(pos.x, pos.y), win)
        else:
            self.sprite = None

    def update(self):
        if self.sprite is not None:
            self.sprite.update()

    def move(self, x, y):
        self.driver.objects[int(self.position.x)][int(self.position.y)] = None
        self.driver.objects[x][y] = self
