import math
from Rendering import *
from graphics import *
from Object import Item
import numpy as np


class Portal(Item):
    """Takes you to the next level."""

    spriteDir = "Portal"

    def onStep(self):
        """Loads next level."""
        self.driver.gameManager.completeLevel()
