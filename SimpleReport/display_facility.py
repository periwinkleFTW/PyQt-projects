from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import sqlite3

import backend

db = backend.Database("simplereport-data.db")



class DisplayFacility(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.setWindowTitle("View facility")
        self.setWindowIcon(QIcon("assets/icons/logo-dark.png"))
        self.setGeometry(450, 150, 750, 650)

        self.Parent = parent

        self.UI()
        self.show()

    def UI(self):
        self.facilityDetails()
        self.widgets()
        self.layouts()

    def facilityDetails(self):

        row = self.Parent.facilitiesTable.currentRow()
        facilityId = self.Parent.facilitiesTable.item(row, 0).text()

        query = "SELECT * FROM facilities WHERE facility_id=?"

        cur = db.cur
        facility = cur.execute(query, (facilityId,)).fetchone()

        self.id = facility[0]
        self.name = facility[1]
        self.location = facility[2]
        self.phone = facility[3]
        self.email = facility[4]
        self.supervisor = facility[5]

    def widgets(self):
        # Top layout widgets
        self.facilityImg = QLabel()
        self.img = QPixmap('assets/icons/logo-dark.png')
        self.facilityImg.setPixmap(self.img)
        self.facilityImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Display facility")
        self.titleText.setAlignment(Qt.AlignCenter)
        # Bottom layout widgets
        self.idEntry = QLabel(str(self.id))
        self.nameEntry = QLineEdit()
        self.nameEntry.setText(self.name)
        self.locationEntry = QLineEdit()
        self.locationEntry.setText(self.location)
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setText(self.phone)
        self.emailEntry = QLineEdit()
        self.emailEntry.setText(self.email)
        self.supervisorEntry = QLineEdit()
        self.supervisorEntry.setText(self.supervisor)
        self.updateBtn = QPushButton("Update")
        self.deleteBtn = QPushButton("Delete")

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        # Add widgets
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.facilityImg)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow("ID: ", self.idEntry)
        self.bottomLayout.addRow("First name: ", self.nameEntry)
        self.bottomLayout.addRow("Last name: ", self.locationEntry)
        self.bottomLayout.addRow("Title: ", self.phoneEntry)
        self.bottomLayout.addRow("Phone: ", self.emailEntry)
        self.bottomLayout.addRow("Email: ", self.supervisorEntry)
        self.bottomLayout.addRow("", self.updateBtn)
        self.bottomLayout.addRow("", self.deleteBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)
