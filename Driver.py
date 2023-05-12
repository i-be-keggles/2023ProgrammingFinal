from graphics import*
from Rendering import*
import random as random
from Player import Player
from Object import Object
from Laser import Laser
from array import *


class Driver:
    win = GraphWin("Game", TileMap.width * TileMap.tileSize, TileMap.height * TileMap.tileSize)

    curTime = time.time()
    frameRate = 12
    timeToFrame = 0

    map = TileMap(win)
    player = Player(map, win)

    objects = [[None]*TileMap.width for i in range(TileMap.height)]

    objects[0][0] = player
    objects[4][4] = Object("Box", Point(4, 4), map, win, "WoodenCrate", True)
    objects[3][6] = Object("Box", Point(3, 6), map, win, "WoodenCrate", True)
    objects[7][4] = Laser("Laser", Point(7, 4), map, win, Point(-1, 0), "Laser")
    objects[2][7] = Laser("Laser", Point(2, 7), map, win, Point(0, -1), "Laser")

    def __init__(self):
        for x in range(self.map.width):
            for y in range(self.map.height):
                if random.random() > 0.3:
                    s = "StoneBrickTile"
                else:
                    s = "DirtTile"
                self.map.setTile(x , y, s)

        for x in range(len(self.objects)):
            for y in range(len(self.objects[x])):
                if self.objects[x][y] is not None:
                    self.objects[x][y].driver = self

    def main(self):
        while self.win.isOpen():
            deltaTime = time.time() - self.curTime
            self.curTime = time.time()
            self.timeToFrame -= deltaTime

            if self.timeToFrame <= 0:
                self.timeToFrame = 1 / self.frameRate

                k = self.win.checkKey()
                if k == "w" or k == "Up":
                    self.player.move(0, -1)
                elif k == "a" or k == "Left":
                    self.player.move(-1, 0)
                elif k == "s" or k == "Down":
                    self.player.move(0, 1)
                elif k == "d" or k == "Right":
                    self.player.move(1, 0)

                self.update()

    def update(self):
        for x in range(len(self.objects)):
            for y in range(len(self.objects[x])):
                if self.objects[x][y] is not None:
                    self.objects[x][y].update()
        # win.redraw()

    def spaceFree(self, x, y):
        return self.objects[int(x)][int(y)] is None


Driver().main()
