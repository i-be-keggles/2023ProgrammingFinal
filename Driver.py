from graphics import*
from Rendering import*


class Driver:
    win = GraphWin("Game", 400, 400)
    s = Sprite("TestSprite1", Point(100, 100), win)
    # s = Sprite("TestSprite2", Point(50, 50), win)

    curTime = time.time()
    frameRate = 24
    timeToFrame = 0

    TileMap(win)

    def main(self):
        while self.win.isOpen():
            deltaTime = time.time() - self.curTime
            self.curTime = time.time()
            self.timeToFrame -= deltaTime

            if self.timeToFrame <= 0:
                self.timeToFrame = 1 / self.frameRate
                update()

    def update(self):
        self.s.Update()
        # win.redraw()

    main()
