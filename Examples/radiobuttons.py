import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(450, 350, 500, 500)
        self.setWindowTitle("Using Radio Buttons")
        self.UI()

    def UI(self):
        self.name = QLineEdit(self)
        self.name.move(150, 50)
        self.name.setPlaceholderText("Name")
        self.surname = QLineEdit(self)
        self.surname.move(150, 80)
        self.surname.setPlaceholderText("Surname")
        self.male = QRadioButton("Male", self)
        self.male.move(150, 110)
        self.female = QRadioButton("Female", self)
        self.female.move(150, 130)

        button = QPushButton("Submit", self)
        button.clicked.connect(self.getValues)
        self.show()

    def getValues(self):
        name = self.name.text()
        surname = self.surname.text()

        if self.male.isChecked():
            print("You are " + name + " " + surname + ". You are male")
        elif self.female.isChecked():
            print("You are " + name + " " + surname + ". You are female")
        else:
            print("You are " + name + " " + surname + ". Gender unknown")



        self.show()



def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
