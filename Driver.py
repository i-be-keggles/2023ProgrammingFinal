from graphics import*
from Rendering import*
import random as random


class Driver:
    win = GraphWin("Game", 400, 400)
    s = Sprite("TestSprite1", Point(100, 100), win)
    # s = Sprite("TestSprite2", Point(50, 50), win)

    curTime = time.time()
    frameRate = 24
    timeToFrame = 0

    map = TileMap(win)

    def __init__(self):
        for x in range(self.map.width):
            for y in range(self.map.height):
                s = ""
                if random.random() > 0.3:
                    s = "StoneBrickTile"
                else:
                    s = "DirtTile"
                self.map.setTile(x , y, s)

    def main(self):
        while self.win.isOpen():
            deltaTime = time.time() - self.curTime
            self.curTime = time.time()
            self.timeToFrame -= deltaTime

            if self.timeToFrame <= 0:
                self.timeToFrame = 1 / self.frameRate
                self.update()
                self.s.move(Point(1, 0))

    def update(self):
        self.s.Update()
        # win.redraw()


Driver().main()
