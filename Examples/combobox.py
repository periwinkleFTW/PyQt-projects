import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(450, 350, 500, 500)
        self.setWindowTitle("Using ComboBox")
        self.UI()

    def UI(self):
        self.combo = QComboBox(self)
        self.combo.move(150, 100)
        button = QPushButton("Save", self)
        button.move(150, 130)
        button.clicked.connect(self.getValue)
        list1 = ["Batman", "Superman", "Hawk"]

        for name in list1:
            self.combo.addItem(name)

        for number in range(18, 101):
            self.combo.addItem(str(number))

        self.show()

    def getValue(self):
        value = self.combo.currentText()
        print(value)



def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
