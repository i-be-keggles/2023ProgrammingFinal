from Rendering import *
from graphics import *


class Object:
    """Base class for physically representable objects in game."""

    driver = None

    def __init__(self, name, pos, tMap, win, sprite=None, kinematic=False):
        self.name = name
        self.position = Point(pos.x, pos.y)
        self.tMap = tMap
        self.win = win
        self.kinematic = kinematic

        if sprite is not None:
            self.sprite = Sprite(sprite, tMap.tileToPoint(pos.x, pos.y), win)
        else:
            self.sprite = None

    def update(self):
        if self.sprite is not None:
            self.sprite.update()

    def move(self, dx, dy):
        """Moves object by (dx, dy) spaces"""

        x, y = int(self.position.x + dx), int(self.position.y + dy)
        self.driver.objects[int(self.position.x)][int(self.position.y)] = None
        self.position = Point(x, y)
        self.driver.objects[x][y] = self
        self.sprite.move(Point(dx * TileMap.tileSize, dy * TileMap.tileSize))
        print(self.name, self.position, self.sprite.position)
