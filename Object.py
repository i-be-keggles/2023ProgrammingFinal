from Rendering import *
from graphics import *


class Object:
    """Base class for physically representable objects in game."""

    driver = None

    crateDescription = "A wooden crate. Try pushing it around!"
    laserDescription = "Lightning bolts that will damage you if you touch them.\nYou can block their path by pushing something in the way."
    lockDescription = "It's locked. Maybe a key would open this..."
    stoneDescription = "A solid stone wall."

    def __init__(self, name, pos, tMap, win, sprite=None, description="", kinematic=False):
        self.name = name
        self.position = Point(pos.x, pos.y)
        self.tMap = tMap
        self.win = win
        self.kinematic = kinematic
        self.description = description

        if sprite is not None:
            self.sprite = Sprite(sprite, tMap.tileToPoint(pos.x, pos.y), win)
        else:
            self.sprite = None

    def update(self):
        """Refreshes graphics."""
        if self.sprite is not None:
            self.sprite.update()

    def move(self, dx, dy):
        """Moves object by (dx, dy) spaces"""

        x, y = int(self.position.x + dx), int(self.position.y + dy)
        self.driver.objects[int(self.position.x)][int(self.position.y)] = None
        self.position = Point(x, y)
        self.driver.objects[x][y] = self
        self.sprite.move(Point(dx * TileMap.tileSize, dy * TileMap.tileSize))

    def tryUseItem(self, item):
        """Base method triggered when item is used on the object."""
        print("Using", item, "on", self.name)
        self.driver.promptBar.displayText("Nothing happened.")
        pass

    def destroy(self):
        self.driver.objects[int(self.position.x)][int(self.position.y)] = None
        self.sprite.undraw()

    @staticmethod
    def instantiate(obj):
        """Spawn in game object"""
        x, y = int(obj.position.x), int(obj.position.y)
        if Object.driver.spaceFree(x, y):
            Object.driver.objects[x][y] = obj
        else:
            print("ERROR: Cannot instantiate,", obj, "at", x, y, " — space occupied.")


class Item(Object):
    """Base class for interactable items in game."""

    def __init__(self, name, pos, tMap, win, sprite, description="", pickup=True):
        super().__init__(name, pos, tMap, win, sprite, description, False)
        self.pickup = pickup

    def onStep(self):
        """Base method triggered when player moves onto item"""
        pass

    @staticmethod
    def instantiate(item):
        """Spawn in game item"""
        x, y = int(item.position.x), int(item.position.y)
        if not Object.driver.itemAt(x, y):
            Object.driver.items[x][y] = item
        else:
            print("ERROR: Cannot instantiate,", item, "at", x, y, " — space occupied.")