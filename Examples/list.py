import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer

font = QFont("Monaco", 16)

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(450, 350, 500, 500)
        self.setWindowTitle("Using List Widget")
        self.UI()

    def UI(self):
        self.add_record = QLineEdit(self)
        self.add_record.move(100, 50)
        self.list_widget = QListWidget(self)
        self.list_widget.move(100, 80)

        list1 = ["Batman", "Superman", "Spiderman"]
        self.list_widget.addItems(list1)

        # for number in range(5, 11):
        #     self.list_widget.addItem(str(number))

        btn_add = QPushButton("Add", self)
        btn_add.move(360, 80)
        btn_add.clicked.connect(self.func_add)
        btn_delete = QPushButton("Delete", self)
        btn_delete.move(360, 110)
        btn_delete.clicked.connect(self.func_delete)
        btn_get = QPushButton("Get", self)
        btn_get.move(360, 140)
        btn_get.clicked.connect(self.func_get)
        btn_delete_all = QPushButton("Delete All", self)
        btn_delete_all.move(360, 170)
        btn_delete_all.clicked.connect(self.func_delete_all)

        self.show()

    def func_add(self):
        value = self.add_record.text()
        self.list_widget.addItem(value)
        self.add_record.setText("")

    def func_delete(self):
        id = self.list_widget.currentRow()
        self.list_widget.takeItem(id)

    def func_get(self):
        id = self.list_widget.currentItem().text()
        print(id)

    def func_delete_all(self):
        self.list_widget.clear()

def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
