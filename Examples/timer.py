import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer

font = QFont("Monaco", 16)

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(450, 350, 500, 500)
        self.setWindowTitle("Using Timer")
        self.UI()

    def UI(self):
        self.color_label = QLabel(self)
        self.color_label.resize(250, 250)
        self.color_label.setStyleSheet("background-color: green")
        self.color_label.move(40, 20)

        btn_start = QPushButton("Start", self)
        btn_start.move(80, 300)
        btn_start.clicked.connect(self.start)
        btn_stop = QPushButton("Stop", self)
        btn_stop.move(150, 300)
        btn_stop.clicked.connect(self.stop)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.change_color)
        self.value = 0

        self.show()

    def change_color(self):
        if self.value == 0:
            self.color_label.setStyleSheet("background-color: yellow")
            self.value = 1
        else:
            self.color_label.setStyleSheet("background-color: black")
            self.value = 0

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
