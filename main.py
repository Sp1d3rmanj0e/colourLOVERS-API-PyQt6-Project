from design import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        

def main():
    app = QApplication([])
    window = Window()

    window.show()
    app.exec()

if __name__ == '__main__':
    main()
