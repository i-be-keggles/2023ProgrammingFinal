import math
from Rendering import *
from graphics import *
from Object import Object
import numpy as np


class Lock(Object):
    """Needs a key to pass through."""

    spriteDir = "Lock"

    def tryUseItem(self, item):
        """Keys delete this object,"""
        if item.lower() == "key":
            self.driver.player.inventory.removeItem(item.lower())
            self.driver.promptBar.displayText("Opened.")
            self.destroy()
        else:
            super().tryUseItem(item)
