from Player import Player
from Object import *
from Laser import Laser
from Lock import Lock
from Portal import Portal
from Utility import *
from graphics import*


class GameManager:
    """Handles game progression, narrative, and score."""

    cesareDir = "Cesare"
    curLevel = 0

    savedItems = []

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

    def loadLevel(self, level, rd=True, keepItems=False):
        """Loads a game level."""
        items = []
        if keepItems:
            items = self.driver.player.inventory.items
            self.savedItems = items
        if rd:
            self.driver.restarting = True
            self.driver.__init__()

        levels = [
            Level([
                Player(1, 3, self.driver.map, self.driver, self.win),
                Object("Stone", Point(2, 1), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(3, 1), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(4, 1), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(5, 1), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(2, 6), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(3, 6), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(4, 6), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(5, 6), self.driver.map, self.win, "Stone", Object.stoneDescription)], [

                Portal("Portal", Point(6, 3), self.driver.map, self.win, "Portal", Item.portalDescription, False)],

                ["Well hello there little traveller,\nyou seem rather alone...", "My name is Cesare!\nWould you care to join my cult?", "No? Have it your way then >:(\nGood luck trying to stop me!"], None),

            Level([
                Player(1, 3, self.driver.map, self.driver, self.win),
                Object("Stone", Point(4, 0), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(4, 1), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(4, 2), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(2, 5), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(2, 6), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(2, 7), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Box", Point(4, 3), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Object("Box", Point(3, 4), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True)], [

                Portal("Portal", Point(6, 3), self.driver.map, self.win, "Portal", Item.portalDescription, False),
                Item("Burger", Point(5, 0), self.driver.map, self.win, "Burger", Item.burgerDescription)],

                None, "Crates can be pushed around by walking into them.\n You can also use the arrow keys to move."),

            Level([
                Player(1, 1, self.driver.map, self.driver, self.win),
                Object("Stone", Point(4, 0), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(4, 1), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(4, 2), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(5, 2), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(7, 2), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(0, 3), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(0, 5), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(0, 6), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(2, 5), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(3, 6), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(3, 7), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(5, 6), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(6, 5), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(7, 5), self.driver.map, self.win, "Stone", Object.stoneDescription),

                Object("Box", Point(1, 4), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Object("Box", Point(1, 6), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Lock("Lock", Point(6, 2), self.driver.map, self.win, "Lock", Object.lockDescription)], [

                Portal("Portal", Point(6, 0), self.driver.map, self.win, "Portal", Item.portalDescription, False),
                Item("LightningStone", Point(7, 6), self.driver.map, self.win, "LightningStone", Item.lightningStoneDescription),
                Item("Key", Point(1, 7), self.driver.map, self.win, "Key", Item.keyDescription),
                Item("Burger", Point(6, 6), self.driver.map, self.win, "Burger", Item.burgerDescription)],

                None, "Use a key to unlock a lock.\n Note, you can only push 1 crate at a time."
            ),
            Level([
                Player(1, 0, self.driver.map, self.driver, self.win),
                Object("Stone", Point(7, 1), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(4, 2), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(6, 2), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(0, 4), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(4, 4), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(5, 4), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(0, 6), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(1, 6), self.driver.map, self.win, "Stone", Object.stoneDescription),


                Object("Box", Point(3, 2), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Object("Box", Point(1, 3), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Object("Box", Point(6, 3), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Lock("Lock", Point(4, 3), self.driver.map, self.win, "Lock", Object.lockDescription),
                Lock("Lock", Point(1, 5), self.driver.map, self.win, "Lock", Object.lockDescription),
                Laser("Laser", Point(0, 2), self.driver.map, self.win, Point(1, 0), "Laser", Object.laserDescription),
                Laser("Laser", Point(7, 6), self.driver.map, self.win, Point(-1, 0), "Laser", Object.laserDescription)], [

                Portal("Portal", Point(4, 7), self.driver.map, self.win, "Portal", Item.portalDescription, False),
                Item("Potion", Point(7, 0), self.driver.map, self.win, "Potion", Item.portalDescription),
                Item("Key", Point(7, 3), self.driver.map, self.win, "Key", Item.keyDescription),
                Item("Burger", Point(0, 5), self.driver.map, self.win, "Burger", Item.burgerDescription)],

                ["You've found the portals! Damn acolytes leaving them around.\nNo matter! Let's see how you fare against some lightning!"], None
            ),
            Level([
                Player(1, 0, self.driver.map, self.driver, self.win),
                Object("Stone", Point(5, 0), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(2, 2), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(6, 2), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(5, 3), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(2, 7), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(6, 7), self.driver.map, self.win, "Stone", Object.stoneDescription),

                Object("Box", Point(3, 1), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Object("Box", Point(4, 1), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Object("Box", Point(6, 1), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Object("Box", Point(0, 2), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Object("Box", Point(4, 2), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Object("Box", Point(0, 3), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Object("Box", Point(3, 6), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Object("Box", Point(4, 6), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Object("Box", Point(5, 6), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Lock("Lock", Point(1, 3), self.driver.map, self.win, "Lock", Object.lockDescription),
                Laser("Laser", Point(7, 4), self.driver.map, self.win, Point(-1, 0), "Laser", Object.laserDescription)], [

                Portal("Portal", Point(5, 1), self.driver.map, self.win, "Portal", Item.portalDescription, False),
                Item("Key", Point(7, 3), self.driver.map, self.win, "Key", Item.keyDescription),
                Item("Burger", Point(3, 7), self.driver.map, self.win, "Burger", Item.burgerDescription),
                Item("Burger", Point(4, 7), self.driver.map, self.win, "Burger", Item.burgerDescription),
                Item("Burger", Point(5, 7), self.driver.map, self.win, "Burger", Item.burgerDescription)],

                None, "Hint: not everything always has to be used.\n But left over items from previous levels may come in handy now..."
            ),
            Level([
                Player(4, 5, self.driver.map, self.driver, self.win),
                Object("Stone", Point(2, 1), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(3, 1), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(5, 2), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(0, 4), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(7, 4), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(2, 6), self.driver.map, self.win, "Stone", Object.stoneDescription),
                Object("Stone", Point(5, 6), self.driver.map, self.win, "Stone", Object.stoneDescription),

                Object("Box", Point(2, 0), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Object("Box", Point(4, 3), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Object("Box", Point(2, 5), self.driver.map, self.win, "WoodenCrate", Object.crateDescription, True),
                Lock("Lock", Point(4, 1), self.driver.map, self.win, "Lock", Object.lockDescription),
                Lock("Lock", Point(0, 5), self.driver.map, self.win, "Lock", Object.lockDescription),
                Laser("Laser", Point(6, 7), self.driver.map, self.win, Point(0, -1), "Laser", Object.laserDescription),
                Laser("Laser", Point(1, 7), self.driver.map, self.win, Point(0, -1), "Laser", Object.laserDescription)],
                [

                    Portal("Portal", Point(0, 7), self.driver.map, self.win, "Portal", Item.portalDescription, False),
                    Portal("Portal", Point(7, 7), self.driver.map, self.win, "Portal", Item.portalDescription, False),
                    Item("Key", Point(3, 7), self.driver.map, self.win, "Key", Item.keyDescription),
                    Item("Burger", Point(5, 0), self.driver.map, self.win, "Burger", Item.burgerDescription),
                    Item("Burger", Point(0, 1), self.driver.map, self.win, "Burger", Item.burgerDescription),
                    Item("Burger", Point(7, 1), self.driver.map, self.win, "Burger", Item.burgerDescription),
                    Item("Burger", Point(7, 5), self.driver.map, self.win, "Burger", Item.burgerDescription),
                    Item("LightningStone", Point(3, 2), self.driver.map, self.win, "LightningStone", Item.lightningStoneDescription)],

                ["No! Stop stealing my burgers!\n I need those for my summoning ritual!", "Why do you keep pushing?\nYou must underestimate my genius.", "Let's see how you handle my traps!\n Which portal can you take, traveller?"], None
            )
        ]

        if len(levels) == self.curLevel:
            self.displayScore()
            return

        self.driver.player = levels[level].objects[0]
        self.promptBar = self.driver.promptBar

        for i in self.savedItems:
            self.driver.player.inventory.pickupItem(i)

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
        self.loadLevel(self.curLevel, keepItems=True)

    def displayScore(self):
        x = 110
        panel = Sprite("InventoryPanel", Point(x, self.win.getHeight()/2), self.win)
        panel.update()
        winText = Text(Point(x, self.win.getHeight()/2 - 50), "YOU WIN!")
        winText.setSize(20)
        winText.draw(self.win)

        score = 0
        for i in self.savedItems:
            if i.name.lower() == "burger":
                score += 1

        scoreText = Text(Point(x, self.win.getHeight()/2 + 10), "Score:\n" + str(score) + " burger" + str(np.where(score == 1, "", "s")) + " collected")
        scoreText.setSize(15)
        scoreText.draw(self.win)

        self.cesare.move(Point(60, 0))

        self.narrate(["Oh you would wouldn't you. You would! I knew-\nI knew you'd pull something like this since I woke up this morning.", "Well you have all my burgers!\n OH I'LL GET YOU FOR THIS TRAVELLERRRRRRRR (next time tho)."])