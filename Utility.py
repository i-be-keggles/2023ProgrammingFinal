from Rendering import *
import numpy as np
#from pyglet import font
#font.add_file("Assets/pixel.tff")


def clamp(a, minimum, maximum):
    """Constrains a to range [min, max]."""
    return min(maximum, max(a, minimum))


class PromptBar:
    """Prompt bar for displaying and inputting text in game."""

    barDir = "PromptBar"

    openY, closedY = TileMap.tileSize/2, -30

    def __init__(self, driver, win):
        self.sprite = Sprite(self.barDir, Point(win.getWidth()/2, win.getHeight() - self.openY), win)
        self.sprite.update()
        self.win = win
        self.driver = driver

        self.textField = None
        self.openField()

        self.text = Text(Point(win.getWidth()/2, win.getHeight() - self.openY), "")
        self.text.draw(win)

        self.t = Text(Point(self.win.getWidth() - 55, self.win.getHeight() - 10), "direction text")
        self.t.setSize(8)
        self.textStack = []

    def update(self):
        """Refreshes graphics."""
        m = self.win.checkMouse()
        if self.textField is None:
            if m is not None:
                if len(self.textStack) == 0:
                    self.text.setText("")
                    self.openField()
                else:
                    self.textStack.remove(self.textStack[0])
                    if len(self.textStack) == 0:
                        self.text.setText("")
                        self.openField()
                    else:
                        self.displayText(self.textStack)
        self.t.setText(np.where(self.textField is None, "click to continue", "press enter to input"))
        self.t.undraw()
        self.t.draw(self.win)

    def getCommand(self):
        """Handles text input."""
        t = self.textField.getText()
        self.textField.setText("")
        return t.lower()

    def openField(self):
        """Activates text input."""
        self.textField = Entry(Point(self.win.getWidth()/2, self.win.getHeight() - self.openY), 50)
        self.textField.setFace("times roman")
        self.textField.setFill("white")
        self.textField.draw(self.win)

    def closeField(self):
        """Deactivates text input."""
        self.textField.setText("")
        self.textField.undraw()
        self.textField = None

    def displayText(self, text, multi=False):
        """Displays text on screen in sequence."""
        if self.textField is not None:
            self.closeField()

        if multi:
            for i in text:
                self.textStack.append(i)

        if len(self.textStack) > 0:
            text = self.textStack[0]
        self.text.setText(text)
        self.t.setText("click to continue")


class Level:
    """Contains information about game levels"""

    def __init__(self, objects, items, dialogue, opening):
        self.objects = objects
        self.items = items
        self.dialogue = dialogue
        self.opening = opening
