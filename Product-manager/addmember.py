import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
from PIL import Image

con = sqlite3.connect("products.db")
cur = con.cursor()

defaultImg = "Resources/img/store.png"

class AddMember(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add member")
        self.setWindowIcon(QIcon("Resources/icons/icon.ico"))
        self.setGeometry(450, 150, 350, 550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # Top layout widgets
        self.addMemberImg = QLabel()
        self.img = QPixmap('Resources/icons/addmember.png')
        self.addMemberImg.setPixmap(self.img)
        self.addMemberImg.setAlignment(Qt.AlignCenter)
        self.title = QLabel("Add member")
        self.title.setAlignment(Qt.AlignCenter)
        # Bottom layout widgets
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Enter name")
        self.surnameEntry = QLineEdit()
        self.surnameEntry.setPlaceholderText("Enter surname")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setPlaceholderText("Enter phone number")
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.clicked.connect(self.addmember)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
        # Add widgets to layouts
        self.topLayout.addWidget(self.title)
        self.topLayout.addWidget(self.addMemberImg)
        self.topFrame.setLayout(self.topLayout)
        self.bottomLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.bottomLayout.addRow(QLabel("Surname: "), self.surnameEntry)
        self.bottomLayout.addRow(QLabel("Phone: "), self.phoneEntry)
        self.bottomLayout.addRow(QLabel(""), self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def addmember(self):
        name = self.nameEntry.text()
        surname = self.surnameEntry.text()
        phone = self.phoneEntry.text()

        if (name and surname and phone != ""):
            try:
                query = "INSERT INTO members (member_name, member_surname, member_phone) " \
                        "VALUES (?, ?, ?)"
                cur.execute(query, (name, surname, phone))
                con.commit()
                QMessageBox.information(self, "Info", "Member has been added")
                self.nameEntry.setText("")
                self.surnameEntry.setText("")
                self.phoneEntry.setText("")
            except:
                QMessageBox.information(self, "Info", "Member has not been added")
        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty")