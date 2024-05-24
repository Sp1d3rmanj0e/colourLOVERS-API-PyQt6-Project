from design import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QColorDialog
import requests

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
            self.label_colorHex.setText(color)
        else:
            print("Dialog cancelled")

    def randomColor(self):
        getRandomColor()
        
# API ACCESSORS
def getRandomColor():

    query = "https://www.colourlovers.com/api/palettes/random?format=json"
    response = requests.get(query) 
    print(response.status_code)

def main():
    app = QApplication([])
    window = Window()

    window.show()
    app.exec()

if __name__ == '__main__':
    main()
