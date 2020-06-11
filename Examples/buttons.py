import sys
from PyQt5.QtWidgets import *


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(450, 350, 350, 350)
        self.setWindowTitle("Using Buttons")
        self.UI()

    def UI(self):
        self.text = QLabel("My text", self)
        enter_button = QPushButton("Enter", self)
        exit_button = QPushButton("Exit", self)
        self.text.move(150, 50)
        enter_button.move(100, 100)
        exit_button.move(200, 100)
        enter_button.clicked.connect(self.enter_func)
        exit_button.clicked.connect(self.exit_func)

        self.show()

    def enter_func(self):
        QApplication.processEvents()
        self.text.setText("Enter")

    def exit_func(self):
        QApplication.processEvents()
        self.text.setText("Exit")


def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
