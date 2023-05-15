from graphics import *
from Rendering import *
from Object import Object
from Utility import clamp


class Player(Object):
    """Player character class."""

    spriteDir = "WizardIdle"
    spriteYOffset = 20

    def __init__(self, x, y, tMap, win):
        super().__init__("Player", Point(x, y), tMap, win)

        self.health = 3
        self.x, self.y = x, y

        self.map = tMap
        self.sprR = Sprite(self.spriteDir, tMap.tileToPoint(self.x, self.y), win)
        self.sprL = Sprite(self.spriteDir, tMap.tileToPoint(self.x, self.y), win, True)
        self.sprite = self.sprR

        self.inventory = Inventory(self.driver, win)

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
        self.driver.promptBar.displayText("You died!")
        self.driver.restartLevel()

    def tryPush(self, x, y, dx, dy):
        """Checks and handles player pushing an object."""
        if not (0 <= x+dx < TileMap.width) or not (0 <= y+dy < TileMap.height) or self.driver.spaceFree(x, y)  or not self.driver.spaceFree(x+dx, y+dy) or not self.driver.objects[x][y].kinematic:
            return False
        else:
            o = self.driver.objects[x][y]
            o.move(int(dx), int(dy))
            return True


class Inventory:
    """Class for inventory management."""

    rows = 2
    columns = 5

    panelDir = "InventoryPanel"
    slotDir = "InventorySlot"
    slotSize = 64
    textMargin = -10

    def __init__(self, driver, win):
        self.items = []
        self.slots = [None]*self.rows*self.columns
        self.text = [None]*self.rows*self.columns

        self.driver = driver
        self.win = win
        self.open = False

        p = Point(win.getWidth()/2, win.getHeight()/2)
        self.panel = Sprite(self.panelDir, p, win)
        sx = self.columns * self.slotSize
        sy = self.rows * self.slotSize
        for x in range(self.columns):
            for y in range(self.rows):
                #print(sx, x*self.slotSize)
                self.slots[x + y*self.columns] = Sprite(self.slotDir, Point(p.x - sx/2 + x*self.slotSize, p.y - sy/2 + y*self.slotSize), win)
                self.text[x + y*self.columns] = Text(Point(p.x - sx/2 + x*self.slotSize, p.y - sy/2 + y*self.slotSize + self.textMargin), "")

    def update(self):
        self.panel.update()
        for i in range(self.columns*self.rows):
            self.slots[i].update()
            if i < len(self.items):
                self.items[i].update()
                self.text[i].draw(self.win)

    def pickupItem(self, item):
        if len(self.items) >= self.columns*self.rows:
            self.driver.promptBar.displayText("Cannot pickup " + item.name + ".\n Inventory full.")
            return None
        try:
            self.driver.items.remove(item)
        except:
            pass
        item.position = self.slots[len(self.items)].position
        self.items.append(item)
        self.text[len(self.items)-1].setText(item.name)

    def openInventory(self):
        self.update()
        self.open = True

    def closeInventory(self):
        self.open = False
        self.panel.undraw()
        for i in range(self.columns * self.rows):
            self.slots[i].undraw()
            if i < len(self.items):
                self.items[i].undraw()
                self.text[i].draw(self.win)