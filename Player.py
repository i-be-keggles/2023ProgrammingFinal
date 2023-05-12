from graphics import *
from Rendering import *
from Object import Object
from Utility import clamp


class Player(Object):
    """Player character class."""

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
        """Moves the player by (x, y) spaces."""
        px = clamp(self.x + x, 0, self.map.width - 1)
        py = clamp(self.y + y, 0, self.map.height - 1)
        if self.driver.spaceFree(px, py) or self.tryPush(px, py, x, y):
            self.x = px
            self.y = py
            p = self.map.tileToPoint(self.x, self.y)
            super().move(x, y)
            self.sprite.move(Point(p.x - self.sprite.position.x, p.y - self.sprite.position.y - self.spriteYOffset))

        if x > 0 and self.sprite == self.sprL:
            self.setSprite(self.sprR)
        if x < 0 and self.sprite == self.sprR:
            self.setSprite(self.sprL)

    def setSprite(self, sprite):
        """Sets the players sprite to another. Can be used for animation changes."""
        self.sprite.undraw()
        sprite.position = self.sprite.position
        self.sprite = sprite
        self.sprite.update()

    def takeDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        print("You died.")

    def tryPush(self, x, y, dx, dy):
        """Checks and handles player pushing an object."""
        if not (0 <= x+dx < TileMap.width) or not (0 <= y+dy < TileMap.height) or self.driver.spaceFree(x, y)  or not self.driver.spaceFree(x+dx, y+dy) or not self.driver.objects[x][y].kinematic:
            return False
        else:
            o = self.driver.objects[x][y]
            o.move(int(dx), int(dy))
            return True