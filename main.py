# from colourlovers.clapi import ColourLovers
# cl = ColourLovers()
# print(cl.search_colors(True, request='random', format = 'json'))

import random

from design import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QColorDialog

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Check if choose color button pressed
        self.pushButton_chooseColor.clicked.connect(self.chooseColor)

        # Check if random color button pressed
        self.pushButton_randomColor.clicked.connect(self.randomColor)
    
    def chooseColor(self):
        dialog = QColorDialog()

        clickedOk = dialog.exec()

        if clickedOk:
            # Get the color chosen from the dialog
            color = dialog.currentColor().name()

            # Set label color to the dialog's chosen color
            self.setNewColor(color)
        else:
            print("Dialog cancelled")

    # Generates and returns a random color
    def getRandomHexColor(self):
        red   = random.randint(0, 255)
        green = random.randint(0, 255)
        blue  = random.randint(0, 255)
        hex = '#%02x%02x%02x' % (red, blue, green) # CREDIT TO: Dietrich Epp --> https://stackoverflow.com/questions/3380726/converting-an-rgb-color-tuple-to-a-hexidecimal-string
        return hex

    # Generates and sets a new random color
    def randomColor(self):
        hex = self.getRandomHexColor()
        self.setNewColor(hex)

    # Changes the seed color title
    # Changes the seed color image
    # Changes the palette collection
    def setNewColor(self, hex):
        self.label_colorHex.setText(hex)

    

def main():
    app = QApplication([])
    window = Window()

    window.show()
    app.exec()

if __name__ == '__main__':
    main()
