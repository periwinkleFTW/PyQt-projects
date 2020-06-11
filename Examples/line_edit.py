import sys
from PyQt5.QtWidgets import *


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(450, 350, 350, 350)
        self.setWindowTitle("Using LineEdit")
        self.UI()

    def UI(self):
        self.name_textbox = QLineEdit(self)
        self.name_textbox.setPlaceholderText("Name")
        self.name_textbox.move(120, 50)
        self.pass_textbox = QLineEdit(self)
        self.pass_textbox.setPlaceholderText("Password")
        self.pass_textbox.setEchoMode(QLineEdit.Password)
        self.pass_textbox.move(120, 80)

        button = QPushButton("Save", self)
        button.move(180, 110)
        button.clicked.connect(self.getValue)

        self.show()

    def getValue(self):
        name = self.name_textbox.text()
        password = self.pass_textbox.text()
        self.setWindowTitle("Your name is: " + name)


def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
