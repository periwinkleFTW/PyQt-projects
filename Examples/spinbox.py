import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

font = QFont("Monaco", 16)

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(450, 350, 500, 500)
        self.setWindowTitle("Using Spin Boxes")
        self.UI()

    def UI(self):
        self.spinbox = QSpinBox(self)
        self.spinbox.move(150, 100)
        self.spinbox.setFont(font)
        self.spinbox.setRange(0, 200)
        self.spinbox.setPrefix("$ ")
        self.spinbox.setSuffix(" thousand")
        self.spinbox.setSingleStep(5)
        #self.spinbox.valueChanged.connect(self.getValue)
        button = QPushButton("Submit", self)
        button.move(150, 140)
        button.clicked.connect(self.getValue)

        self.show()

    def getValue(self):
        value = self.spinbox.value()
        print(value)



def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
