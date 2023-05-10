from graphics import *
from Rendering import *
from Object import Object
from Utility import clamp


class Player(Object):
    health = 3
    x, y = 0, 0
    spriteDir = "WizardIdle"
    spriteYOffset = 20

    def __init__(self, tMap, win):
        super().__init__("Player", Point(0, 0), tMap, win)
        self.map = tMap
        self.sprR = Sprite(self.spriteDir, tMap.tileToPoint(self.x, self.y), win)
        self.sprL = Sprite(self.spriteDir, tMap.tileToPoint(self.x, self.y), win, True)
        self.sprite = self.sprR

    def update(self):
        self.sprite.update()

    def move(self, x, y):
        px = clamp(self.x + x, 0, self.map.width - 1)
        py = clamp(self.y + y, 0, self.map.height - 1)
        if self.driver.spaceFree(px, py):
            self.x = px
            self.y = py
            p = self.map.tileToPoint(self.x, self.y)
            self.sprite.move(Point(p.x - self.sprite.position.x, p.y - self.sprite.position.y - self.spriteYOffset))
            super().move(x, y)

        if x > 0 and self.sprite == self.sprL:
            self.setSprite(self.sprR)
        if x < 0 and self.sprite == self.sprR:
            self.setSprite(self.sprL)

    def setSprite(self, sprite):
        self.sprite.undraw()
        sprite.position = self.sprite.position
        self.sprite = sprite
        self.sprite.update()
