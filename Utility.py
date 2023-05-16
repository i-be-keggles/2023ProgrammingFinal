from Rendering import *
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

        self.t = Text(Point(self.win.getWidth() - 50, self.win.getHeight() - 10), "enter to continue")
        self.t = Text(Point(self.win.getWidth() - 50, self.win.getHeight() - 100), "enter to continue")
        self.t.setSize(8)
        self.textStack = []

    def update(self):
        """Refreshes graphics."""
        print(self.textField)
        if self.textField is None:
            if self.win.checkMouse() is not None:
                if len(self.textStack) == 0:
                    self.text.setText("")
                    self.t.setText("")
                    self.openField()
                else:
                    self.textStack.remove(self.textStack[0])
                    self.displayText(self.textStack)
                    self.update()
            self.t.setText("click to continue")

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
