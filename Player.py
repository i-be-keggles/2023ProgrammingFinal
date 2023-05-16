from graphics import *
from Rendering import *
from Object import Object
from Utility import clamp


class Player(Object):
    """Player character class."""

    spriteDir = "WizardIdle"
    spriteYOffset = 20

    def __init__(self, x, y, tMap, driver, win):
        super().__init__("Player", Point(x, y), tMap, win)

        self.health = 3
        self.x, self.y = x, y

        self.map = tMap
        self.sprR = Sprite(self.spriteDir, tMap.tileToPoint(self.x, self.y), win)
        self.sprL = Sprite(self.spriteDir, tMap.tileToPoint(self.x, self.y), win, True)
        self.sprite = self.sprR
        self.driver = driver

        self.inventory = Inventory(self.driver, win)

        self.dx, self.dy = 0, 0

    def update(self):
        """Refreshes graphics."""
        self.sprite.update()

    def move(self, x, y):
        """Moves the player by (x, y) spaces."""
        self.dx, self.dy, = x, y
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

        if self.inventory.open:
            self.inventory.closeInventory()

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
        if self.inventory.containsItem("Potion"):
            self.inventory.removeItem("Potion")
            self.move(-self.dx, -self.dy)
            self.driver.promptBar.displayText("A potion saved your life!")
        else:
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

    def tryPickup(self):
        """Checks and handles player picking up an item."""
        if not self.driver.itemAt(self.x, self.y):
            return False
        self.inventory.pickupItem(self.driver.items[self.x][self.y])


class Inventory:
    """Class for inventory management."""

    rows = 2
    columns = 5

    panelDir = "InventoryPanel"
    slotDir = "InventorySlot"
    slotSize = 70
    textMargin = 0
    yBuffer = 20

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
        sy = self.rows * (self.slotSize + self.yBuffer)
        for x in range(self.columns):
            for y in range(self.rows):
                #print(sx, x*self.slotSize)
                self.slots[x + y*self.columns] = Sprite(self.slotDir, Point(p.x - sx/2 + (x+0.5)*self.slotSize, p.y - sy/2 + (y+0.5)*(self.slotSize + self.yBuffer)), win)
                self.text[x + y*self.columns] = Text(Point(p.x - sx/2 + (x+0.5)*self.slotSize, p.y - sy/2 + (y+1)*(self.slotSize + self.yBuffer) + self.textMargin), "")

    def update(self):
        """Refreshes graphics."""
        self.panel.update()
        for i in range(self.columns*self.rows):
            self.slots[i].update()
            if i < len(self.items):
                self.items[i].update()
                self.text[i].draw(self.win)

    def pickupItem(self, item):
        """Adds item to inventory."""
        if len(self.items) >= self.columns*self.rows:
            self.driver.promptBar.displayText("Cannot pickup " + item.name + ".\n Inventory full.")
            return None

        self.driver.items[int(item.position.x)][int(item.position.y)] = None

        p = self.slots[len(self.items)].position
        item.sprite.position = p
        item.update()
        if not self.open:
            item.sprite.undraw()
        self.items.append(item)
        print(self.items, self.driver.items)
        self.text[len(self.items)-1].setText(item.name)

    def removeItem(self, item):
        """Removes item from inventory."""
        f = False
        for i in range(len(self.items)):
            if f:
                self.items[i-1].sprite.position = self.slots[i-1].position
                self.text[i-1].setText(self.items[i-1].name)
                self.text[i].setText("")
            elif self.items[i].name.lower() == item.lower():
                f = True
                self.items[i].sprite.undraw()
                self.items.remove(self.items[i])

    def containsItem(self, item):
        """Checks if player is carrying a certain item."""
        for i in self.items:
            if item.lower() == i.name.lower():
                return True
        return False

    def openInventory(self):
        self.update()
        self.open = True

    def closeInventory(self):
        self.open = False
        self.panel.undraw()
        for i in range(self.columns * self.rows):
            self.slots[i].undraw()
            if i < len(self.items):
                self.items[i].sprite.undraw()
                self.text[i].undraw()