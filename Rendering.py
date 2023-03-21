import os
import tkinter

from graphics import*
from PIL import Image as p_image


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
            #self.image = scaleImage(self.image, 2)         # breaks it for some reason
            self.image.draw(self.win)

    def move(self, d):
        self.position = Point(self.position.x + d.x, self.position.y + d.y)


class TileMap:
    """A TileMap is an ordered grid of sprites."""

    tileSize = 64   # in pixels
    width = 10      # in tiles
    height = 10     # in tiles
    map = [[None] * height] * width
    win = None

    def __init__(self, win, tileSize=64, width=5, height=5):
        print(map)
        self.win = win
        self.tileSize = tileSize
        self.width = width
        self.height = height

    def setTile(self, x, y, tile):
        """This function set's grid[x[y]] to the specified tile."""
        self.map[x][y] = Image(Point((x + 0.5) * self.tileSize, (y + 0.5) * self.tileSize), "Assets/Tiles/" + tile + ".png")
        self.map[x][y] = scaleImage(self.map[x][y], 2)
        self.map[x][y].draw(self.win)


def scaleImage(image, size):
    """This function takes and returns duplicate scaled by a factor of given size"""
    scaledImage = Image(image.getAnchor(), image.getWidth()*size, image.getHeight()*size)
    for x in range(scaledImage.getWidth()):
        for y in range(scaledImage.getHeight()):
            c = image.getPixel(int(x/size), int(y/size))
            scaledImage.setPixel(x, y, color_rgb(c[0], c[1], c[2]) )
    return scaledImage
