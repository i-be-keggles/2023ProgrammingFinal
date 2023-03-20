import os
from graphics import*


class Sprite:
    """A Sprite is an animatable collection of images to be displayed and manipulated."""

    image = None
    source = "Assets/Sprites/"
    frames = []
    frame = 0
    position = Point(0,0)
    win = None

    def __init__(self, source, position, graphWin):
        self.source += source
        self.frames = [self.source + "/" + s for s in os.listdir(self.source)]
        self.image = Image(position, self.frames[0])
        self.position = position
        self.win = graphWin
        
    def Update(self):
        d = self.image.getAnchor()
        self.image.move(d.x - self.position.x, d.y - self.position.y)

        if len(self.frames) > 0:
            self.image.undraw()
            self.frame += 1
            if self.frame == len(self.frames):
                self.frame = 0
            self.image = Image(self.position, self.frames[self.frame])
            self.image.draw(self.win)

        def move(d):
            self.position = Point(self.position.x + d.x, self.position.y + d.y)


class TileMap:
    """A TileMap is an ordered grid of sprites."""

    tileSize = 32   # in pixels
    width = 10      # in tiles
    height = 10     # in tiles
    map = [[None] * height] * width
    win = None

    def __init__(self, win, tileSize=32, width=10, height=10):
        print(map)
        self.win = win
        self.tileSize = tileSize
        self.width = width
        self.height = height
