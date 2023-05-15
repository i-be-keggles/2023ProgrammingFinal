import math

from Rendering import *
from graphics import *
from Object import Object
import numpy as np

class Laser(Object):
    """Emits a laserbeam that hurts the player"""

    spriteDir = "Laserbeam"

    def __init__(self,  name, pos, tMap, win, dir, sprite=None, kinematic=False):
        self.x = int(dir.x)
        self.y = int(dir.y)
        self.beam = []
        super().__init__(name, pos, tMap, win, sprite, kinematic)
        self.spriteDir += str(np.where(dir.x != 0, "/Horizontal", "/Vertical"))

        for i in range(int(np.where(self.x != 0, np.where(self.x > 0, TileMap.width - self.position.x, self.position.x), np.where(self.y > 0, TileMap.height - self.position.y, self.position.y)))):
            self.beam.append(Sprite(self.spriteDir, self.tMap.tileToPoint(self.position.x + (i + 1) * self.x, self.position.y + (i + 1) * self.y), self.win))
            self.curL = i

    def update(self):
        super().update()
        h = False
        for i in range(len(self.beam)):
            if self.driver.spaceFree(self.position.x + (i+1) * self.x, self.position.y + (i+1) * self.y) and not h:
                self.beam[i].update()
                self.curL = i
            else:
                if not h and self.driver.objects[int(self.position.x + (i+1) * self.x)][int(self.position.y + (i+1) * self.y)] == self.driver.player:
                #if not h and self.driver.player.position == (int(self.position.x + (i+1) * self.x), int(self.position.y + (i+1) * self.y)):
                    self.driver.player.takeDamage(math.inf)
                h = True
                self.beam[i].undraw()
