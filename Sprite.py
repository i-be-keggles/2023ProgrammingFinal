import os

from graphics import*


class Sprite:
    image = Image(None)
    source = ""
    frames = []
    position = Point(0,0)
    win = None

    def __init__(self, source, position, graphWin):
        self.source = source
        self.frames = os.listdir(source)
        self.image = Image(position, self.frames[0])
        self.position = position
        self.win = graphWin
        
    def Update(self):
        d = self.image.getAnchor() - self.position
        self.image.move(d.x, d.y)
        self.image.draw(self.win)