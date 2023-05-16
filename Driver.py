from graphics import*
from Rendering import*
import random as random
from Player import Player
from Object import *
from Laser import Laser
from Lock import Lock
from Utility import PromptBar
import numpy as np
#from pyglet import font
#font.add_file("Assets/pixel.tff")


class Driver:
    """Base class that runs the game."""
    win = GraphWin("Game", TileMap.width * TileMap.tileSize, (TileMap.height + 1) * TileMap.tileSize)

    curTime = time.time()
    frameRate = 12
    timeToFrame = 0

    performanceMode = False

    if performanceMode:
        win.autoflush = False
        frameRate = 24

    def __init__(self):
        self.map = TileMap(self.win)
        self.player = Player(4, 0, self.map, self, self.win)

        self.objects = [[None] * TileMap.width for i in range(TileMap.height)]
        self.items = [[None] * TileMap.width for i in range(TileMap.height)]

        Object.driver = self
        for x in range(self.map.width):
            for y in range(self.map.height):
                if random.random() > 0.3:
                    s = "StoneBrickTile"
                else:
                    s = "DirtTile"
                self.map.setTile(x, y, s)

        for x in range(len(self.objects)):
            for y in range(len(self.objects[x])):
                if self.objects[x][y] is not None:
                    pass
                    self.objects[x][y].driver = self

        Object.instantiate(self.player)
        Object.instantiate(Object("Box", Point(4, 4), self.map, self.win, "WoodenCrate", Object.crateDescription, True))
        Object.instantiate(Object("Box", Point(3, 6), self.map, self.win, "WoodenCrate", Object.crateDescription, True))
        Object.instantiate(Laser("Laser", Point(7, 4), self.map, self.win, Point(-1, 0), "Laser", Object.laserDescription))
        Object.instantiate(Laser("Laser", Point(2, 7), self.map, self.win, Point(0, -1), "Laser", Object.laserDescription))
        Object.instantiate(Lock("Lock", Point(0, 3), self.map, self.win, "Lock", Object.lockDescription))

        Item.instantiate(Item("Potion", Point(0, 0), self.map, self.win, "Potion", "Stops you from dying once."))
        Item.instantiate(Item("Key", Point(5, 6), self.map, self.win, "Key", "Unlocks a barrier."))
        Item.instantiate(Item("LightningStone", Point(7, 2), self.map, self.win, "LightningStone", "Disables a lightning bolt"))

        #self.player.inventory.pickupItem(Item("Burger", Point(0,0), self.map, self.win, "Burger", "It's a burger."))

        self.promptBar = PromptBar(self, self.win)
        self.promptBar.displayText("Don't touch the lasers!")

        self.main()

    def main(self):
        """Handles main input loop."""
        while self.win.isOpen():
            deltaTime = time.time() - self.curTime
            self.curTime = time.time()
            self.timeToFrame -= deltaTime

            if self.timeToFrame <= 0:
                self.timeToFrame = 1 / self.frameRate

                k = self.win.checkKey()
                if self.promptBar.textField is None or self.promptBar.textField.getText() == "":
                    if k == "w" or k == "Up":
                        self.player.move(0, -1)
                    elif k == "a" or k == "Left":
                        self.player.move(-1, 0)
                    elif k == "s" or k == "Down":
                        self.player.move(0, 1)
                    elif k == "d" or k == "Right":
                        self.player.move(1, 0)
                    elif k == "r":
                        self.restartLevel()
                    elif k == "p":
                        self.win.autoflush = not self.win.autoflush
                elif k == "Return":
                    self.tryCommand(self.promptBar.getCommand())

                self.promptBar.update()
                self.update()

    def update(self):
        """Refreshes graphics."""
        if self.player.inventory.open:
            return
        for x in range(len(self.objects)):
            for y in range(len(self.objects[x])):
                if self.objects[x][y] is not None:
                    self.objects[x][y].update()
                if self.items[x][y] is not None:
                    self.items[x][y].update()

    def spaceFree(self, x, y):
        """Checks for object at position."""
        if not (0 <= x < self.map.width) or not (0 <= y < self.map.height):
            return None
        return self.objects[int(x)][int(y)] is None

    def itemAt(self, x, y):
        """Checks for item at position."""
        if not (0 <= x < self.map.width) or not (0 <= y < self.map.height):
            return None
        return self.items[int(x)][int(y)] is not None

    def restartLevel(self):
        #self.win.close()
        Driver()

    def tryCommand(self, c):
        """Interprets text input."""
        x, y = self.player.x, self.player.y
        s = c.split(" ")

        if c == "go up" or c == "go north" or c == "up":
            self.player.move(0, -1)
        elif c == "go left" or c == "go west" or c == "left":
            self.player.move(-1, 0)
        elif c == "go down" or c == "go south" or c == "down":
            self.player.move(0, 1)
        elif c == "go right" or c == "go east" or c == "right":
            self.player.move(1, 0)

        elif c == "look up":
            if self.spaceFree(x, y - 1) == False:
                self.promptBar.displayText(self.objects[x][y-1].description)
            else:
                self.promptBar.displayText("There's nothing there.")
        elif c == "look left":
            if self.spaceFree(x - 1, y) == False:
                self.promptBar.displayText(self.objects[x-1][y].description)
            else:
                self.promptBar.displayText("There's nothing there.")
        elif c == "look down":
            if self.spaceFree(x, y + 1) == False:
                self.promptBar.displayText(self.objects[x][y+1].description)
            else:
                self.promptBar.displayText("There's nothing there.")
        elif c == "look right":
            if self.spaceFree(x + 1, y) == False:
                self.promptBar.displayText(self.objects[x+1][y].description)
            else:
                self.promptBar.displayText("There's nothing there.")

        elif c == "open inventory":
            self.player.inventory.openInventory()
        elif c == "close inventory":
            self.player.inventory.closeInventory()

        elif c == "pick up":
            if self.player.tryPickup() == False:
                self.promptBar.displayText("There's nothing there.")

        elif len(s) == 3 and s[0] == "use" and (s[2] == "up" or s[2] == "down" or s[2] == "left" or s[2] == "right"):
            self.player.inventory.closeInventory()
            x, y = x + np.where(s[2] == "right", 1, np.where(s[2] == "left", -1, 0)), y + np.where(s[2] == "down", 1, np.where(s[2] == "up", -1, 0))
            if self.spaceFree(x,y) == False:
                if self.player.inventory.containsItem(s[1]):
                    self.objects[x][y].tryUseItem(s[1])
                else:
                    self.promptBar.displayText("You don't have a " + s[1] + ".")
            else:
                self.promptBar.displayText("There's nothing there.")

        elif c == "restart":
            self.restartLevel()
        elif c == "performance":
            self.win.autoflush = not self.win.autoflush

        elif c == "help":
            self.promptBar.displayText("go up/down/left/right, look up/down/left/right, restart, performance, help,\nopen/close inventory, pick up, use [item] up/down/left/right")
        else:
            self.promptBar.displayText("Invalid command.\nUse 'help' for list of commands.")


Driver()
