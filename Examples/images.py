import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(450, 350, 500, 500)
        self.setWindowTitle("Using LineEdit")
        self.UI()

    def UI(self):
        self.image = QLabel(self)
        self.image.setPixmap(QPixmap('../employee-app/icons/logo-dark.png'))
        self.image.move(150, 50)
        remove_btn = QPushButton("Remove", self)
        remove_btn.move(150, 220)
        remove_btn.clicked.connect(self.remove_img)
        show_btn = QPushButton("Show", self)
        show_btn.move(260, 220)
        show_btn.clicked.connect(self.show_img)
        self.show()

    def remove_img(self):
        QApplication.processEvents()
        self.image.close()

    def show_img(self):
        QApplication.processEvents()
        self.image.show()



        self.show()




def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
