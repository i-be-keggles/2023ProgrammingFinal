from graphics import *
from Rendering import *


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

        self.t = Text(Point(self.win.getWidth() - 50, self.win.getHeight() - 10), "click to continue")
        self.t.setSize(8)

    def update(self):
        if self.textField is None and self.win.checkMouse() is not None:
            self.text.setText("")
            self.t.setText("")
            self.openField()

    def getCommand(self):
        t = self.textField.getText()
        self.textField.setText("")
        return t.lower()

    def openField(self):
        self.textField = Entry(Point(self.win.getWidth()/2, self.win.getHeight() - self.openY), 50)
        self.textField.setFace("times roman")
        self.textField.setFill("white")
        self.textField.draw(self.win)

    def closeField(self):
        self.textField.setText("")
        self.textField.undraw()
        self.textField = None

    def displayText(self, text):
        if self.textField is not None:
            self.closeField()

        self.text.setText(text)
        self.t.setText("click to continue")
