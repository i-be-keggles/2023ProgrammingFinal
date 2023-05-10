import os
import tkinter

from graphics import*
# from PIL import Image as p_image


class Sprite:
    """A Sprite is an animatable collection of images to be displayed and manipulated."""

    image = None
    source = "Assets/Sprites/"
    frames = []
    frame = 0
    position = Point(0, 0)
    win = None

    def __init__(self, source, position, graphWin, flip=False):
        self.source += source
        self.frames = [self.source + "/" + s for s in os.listdir(self.source)]
        for x in range(len(self.frames)):
            self.frames[x] = Image(self.position, self.frames[x])
            self.frames[x] = scaleImage(self.frames[x], 2, flip)
        self.image = self.frames[0]
        self.position = position
        self.win = graphWin
        
    def update(self):
        d = self.image.getAnchor()
        self.image.move(d.x - self.position.x, d.y - self.position.y)

        if len(self.frames) > 0:
            self.image.undraw()
            self.frame += 1
            if self.frame == len(self.frames):
                self.frame = 0
            self.image = self.frames[self.frame]

            p = self.image.getAnchor()
            self.image.move(self.position.x - p.x, self.position.y - p.y)
            self.image.draw(self.win)

    def move(self, d):
        self.position = Point(self.position.x + d.x, self.position.y + d.y)

    def undraw(self):
        self.image.undraw()


class TileMap:
    """A TileMap is an ordered grid of sprites."""

    tileSize = 64   # in pixels
    width = 8      # in tiles
    height = 8     # in tiles
    map = [[None] * height] * width
    win = None

    def __init__(self, win, tileSize=64, width=width, height=height):
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

    def tileToPoint(self, x, y):
        return Point((x + 0.5) * self.tileSize, (y + 0.5) * self.tileSize)


def scaleImage(image, size, flip=False):
    """This function takes and returns duplicate scaled by a factor of given size.\nBlack pixels count as alpha=0."""
    scaledImage = Image(image.getAnchor(), image.getWidth()*size, image.getHeight()*size)
    for x in range(scaledImage.getWidth()):
        for y in range(scaledImage.getHeight()):
            if not flip:
                c = image.getPixel(int(x/size), int(y/size))
            else:
                c = image.getPixel(int(image.getWidth() - 1 - (x/size)), int(y/size))
            if c[0] != 0 or c[1] != 0 or c[2] != 0:
                scaledImage.setPixel(x, y, color_rgb(c[0], c[1], c[2]) )
    return scaledImage
