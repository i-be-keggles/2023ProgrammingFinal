from Rendering import *
from graphics import *
from Object import Object
import numpy as np

class Laser(Object):
    """Emits a laserbeam that hurts the player"""

    spriteDir = "Laserbeam"
    beam = []

    def __init__(self,  name, pos, tMap, win, dir, sprite=None, kinematic=False):
        self.x = int(dir.x)
        self.y = int(dir.y)
        super().__init__(name, pos, tMap, win, sprite, kinematic)
        self.spriteDir += str(np.where(dir.x != 0, "/Horizontal", "/Vertical"))

    def update(self):
        super().update()
        l = np.where(self.x != 0, np.where(self.x > 0, TileMap.width - self.position.x, self.position.x), np.where(self.y > 0, TileMap.height - self.position.y, self.position.y))
        for i in range(int(l)):
            if self.driver.spaceFree(self.position.x + (i+1) * self.x, self.position.y + (i+1) * self.y):
                if len(self.beam) == i:
                    self.beam.append(Sprite(self.spriteDir, self.tMap.tileToPoint(self.position.x + (i+1) * self.x, self.position.y + (i+1) * self.y), self.win))
                self.beam[i].update()
            else:
                for x in range(len(self.beam) - 1, i-1, -1):
                    self.beam[i].undraw()
                    self.beam.remove(self.beam[i])
                break
