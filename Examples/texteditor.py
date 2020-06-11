import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

font = QFont("Monaco", 16)

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(450, 350, 500, 500)
        self.setWindowTitle("Using Text Editor")
        self.UI()

    def UI(self):
        self.editor = QTextEdit(self)
        self.editor.move(150, 80)
        self.editor.setAcceptRichText(False)
        button = QPushButton("Send", self)
        button.move(330, 280)
        button.clicked.connect(self.getValue)

        self.show()

    def getValue(self):
        text = self.editor.toPlainText()
        print(text)


def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
