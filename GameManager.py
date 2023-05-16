from Player import Player
from Object import *
from Laser import Laser
from Lock import Lock
from Portal import Portal
from Utility import *


class GameManager:
    """Handles game progression, narrative, and score."""

    cesareDir = "Cesare"
    curLevel = 0

    def __init__(self, driver, win):
        self.driver = driver
        self.win = win
        self.promptBar = driver.promptBar
        self.narrating = False
        self.cesare = Sprite(self.cesareDir, Point(win.getWidth()/2 + 50, win.getHeight()/2 - 40), win)

    def update(self):
        """Refreshes graphics."""
        if self.narrating and len(self.promptBar.textStack) == 0:
            self.narrating = False
            self.cesare.undraw()

    def narrate(self, text):
        """Displays text as narrative dialogue."""
        for i in range(len(text)):
            text[i] = '"' + text[i] + '"'
        text[0] = "Cesare: " + text[0]
        self.narrating = True
        self.cesare.update()
        self.promptBar.displayText(text, True)

    def loadLevel(self, level, rd=True):
        """Loads a game level."""
        if rd:
            self.driver.restarting = True
            self.driver.__init__()

        levels = [Level([
            Player(4, 0, self.driver.map, self.driver, self.win),
            Object("Box", Point(4, 4), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
            Object("Box", Point(3, 6), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
            Laser("Laser", Point(7, 4), self.driver.map, self.win, Point(-1, 0), "Laser", Object.laserDescription),
            Laser("Laser", Point(2, 7), self.driver.map, self.win, Point(0, -1), "Laser", Object.laserDescription),
            Lock("Lock", Point(0, 3), self.driver.map, self.win, "Lock", Object.lockDescription)], [

            Item("Potion", Point(0, 0), self.driver.map, self.win, "Potion", "Stops you from dying once."),
            Item("Key", Point(5, 6), self.driver.map, self.win, "Key", "Unlocks a barrier."),
            Item("LightningStone", Point(7, 2), self.driver.map, self.win, "LightningStone", "Disables a lightning bolt"),
            Portal("Portal", Point(0, 6), self.driver.map, self.win, "Portal", "Takes you to the next level.", False)],

            ["Well hello there little traveler,\nyou seem rather alone...", "My name is Cesare!\nWould you care to join my cult?", "No? Have it your way then >:(\nGood luck trying to stop me!"], None),

            Level([
                Player(0, 3, self.driver.map, self.driver, self.win),
                Object("Box", Point(4, 4), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Object("Box", Point(3, 6), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Object("Stone", Point(5,5), self.driver.map, self.win, "Stone", Object.stoneDescription)], [

                ],

                None, "Crates can be pushed around by walking into them."
            )
        ]

        self.driver.player = levels[level].objects[0]
        self.promptBar = self.driver.promptBar

        for o in levels[level].objects:
            Object.instantiate(o)
        for i in levels[level].items:
            Item.instantiate(i)
        if levels[level].dialogue is not None:
            self.narrate(levels[level].dialogue)
        elif levels[level].opening is not None:
            self.promptBar.displayText(levels[level].opening)

        self.driver.restarting = False
        self.driver.main()

    def completeLevel(self):
        """Handles level completion."""
        self.curLevel += 1

        self.loadLevel(self.curLevel)
