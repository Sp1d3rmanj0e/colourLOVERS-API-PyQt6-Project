import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

class Example(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Hide Widget Example')
        
        self.btn_hide = QPushButton('Hide Widget', self)
        self.btn_hide.clicked.connect(self.hideWidget)
        self.btn_hide.setGeometry(10, 10, 100, 30)
        
        self.widget_to_hide = QPushButton('Widget to Hide', self)
        self.widget_to_hide.setGeometry(10, 50, 100, 100)
        
        self.show()
        
    def hideWidget(self):
        self.widget_to_hide.hide()  # Hide the widget

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
