from graphics import*
from Rendering import*
import random as random
from Player import Player


class Driver:
    win = GraphWin("Game", TileMap.width * TileMap.tileSize, TileMap.height * TileMap.tileSize)

    curTime = time.time()
    frameRate = 24
    timeToFrame = 0

    map = TileMap(win)
    player = Player(map, win)

    sprites = []

    sprites.append(player.sprite)
    #sprites.append(Sprite("TestSprite1", Point(200, 200), win))

    def __init__(self):
        for x in range(self.map.width):
            for y in range(self.map.height):
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

                k = self.win.checkKey()
                if k == "w":
                    self.player.move(0, -1)
                elif k == "a":
                    self.player.move(-1, 0)
                elif k == "s":
                    self.player.move(0, 1)
                elif k == "d":
                    self.player.move(1, 0)

                self.update()

    def update(self):
        for sprite in self.sprites:
            sprite.Update()
        # win.redraw()


Driver().main()
