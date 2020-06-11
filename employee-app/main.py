from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import sqlite3

conn = sqlite3.connect("employees.db")


class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Employees")
        self.setGeometry(450, 150, 750, 600)

        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()

    def mainDesign(self):
        self.employeeList = QListWidget()
        self.btnNew = QPushButton("New")
        self.btnNew.clicked.connect(self.addEmployee)
        self.btnUpdate = QPushButton("Update")
        self.btnUpdate.clicked.connect(self.updateEmployee)
        self.btnDelete = QPushButton("Delete")
        self.btnDelete.clicked.connect(self.deleteEmployee)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.leftLayout = QFormLayout()
        self.rightMainLayout = QVBoxLayout()
        self.rightTopLayout = QHBoxLayout()
        self.rightBottomLayout = QHBoxLayout()

        # Nesting secondary layouts
        self.rightMainLayout.addLayout(self.rightTopLayout)
        self.rightMainLayout.addLayout(self.rightBottomLayout)
        # Adding layouts to the main layout, put percentage of the fill after the comma
        self.mainLayout.addLayout(self.leftLayout, 40)
        self.mainLayout.addLayout(self.rightMainLayout, 60)

        # Add widgets to the right layout. List to the top and btns to the bottom layouts
        self.rightTopLayout.addWidget(self.employeeList)
        self.rightBottomLayout.addWidget(self.btnNew)
        self.rightBottomLayout.addWidget(self.btnUpdate)
        self.rightBottomLayout.addWidget(self.btnDelete)

        self.setLayout(self.mainLayout)

    def addEmployee(self):
        self.newEmployee = AddEmployee()
        # Close main window
        self.close()

    def updateEmployee(self):
        pass

    def deleteEmployee(self):
        pass


class AddEmployee(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Employee")
        self.setGeometry(450, 150, 350, 600)
        self.UI()
        self.show()

    def UI(self):
        pass

    def mainDesign(self):
        self.title = QLabel("Add person")
        self.title.setStyleSheet("font-size: 24pt; font-family: Arial Bold")
        self.imgAdd = QLabel()
        self.imgAdd.setPixmap(QPixmap("/icons/logo-dark.png"))

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

        # Adding widgets to layout
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.title)
        self.topLayout.addWidget(self.imgAdd)
        self.topLayout.addStretch()

        self.setLayout(self.mainLayout)


def main():
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
