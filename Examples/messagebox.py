import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

font = QFont("Monaco", 12)

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(450, 350, 500, 500)
        self.setWindowTitle("Using Message Boxes")
        self.UI()

    def UI(self):
        button = QPushButton("Click me", self)
        button.setFont(font)
        button.move(200, 150)
        button.clicked.connect(self.message_box)
        self.show()

    def message_box(self):
        # mbox = QMessageBox.question(self, "Warning", "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        # if mbox == QMessageBox.Yes:
        #     sys.exit()
        # elif mbox == QMessageBox.No:
        #     print("You clicked NO")
        mbox = QMessageBox.information(self, "Information", "You logged out")




def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
