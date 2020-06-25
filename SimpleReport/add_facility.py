import sys, os
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import sqlite3
from PIL import Image

import backend

db = backend.Database("simplereport-data.db")

# conn = sqlite3.connect("simplereport-data.db")
# cur = conn.cursor()

defaultImg = "assets/icons/logo-dark.png"

class AddFacility(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add facility")
        self.setWindowIcon(QIcon("assets/icons/icon.ico"))
        self.setGeometry(450, 150, 750, 650)
        #self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # Top layout widgets
        self.addFacilityImg = QLabel()
        self.img = QPixmap('assets/icons/add-facility.png')
        self.addFacilityImg.setPixmap(self.img)
        self.addFacilityImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Add facility")
        self.titleText.setAlignment(Qt.AlignCenter)
        # Bottom layout widgets
        self.facilityInfoTitleText = QLabel("Facility info")
        self.facilityInfoTitleText.setAlignment(Qt.AlignCenter)
        self.facilityIdEntry = QLineEdit()
        self.facilityNameEntry = QLineEdit()
        self.facilityLocationEntry = QLineEdit()
        self.facilityPhoneEntry = QLineEdit()
        self.facilityEmailEntry = QLineEdit()
        self.facilitySupervisorEntry = QLineEdit()

        self.attachPhotoBtn = QPushButton("Attach photo")

        self.addFacilityBtn = QPushButton("Add facility")
        self.addFacilityBtn.clicked.connect(self.addFacility)


    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        # Put elements into frames for visual distinction
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        # Add widgets to top layout
        self.topLayout.addWidget(self.addFacilityImg)
        self.topLayout.addWidget(self.titleText)

        self.topFrame.setLayout(self.topLayout)

        # Add widgets to middle layout
        self.bottomLayout.addWidget(self.facilityInfoTitleText)
        self.bottomLayout.addRow(QLabel("Facility ID: "), self.facilityIdEntry)
        self.bottomLayout.addRow(QLabel("Facility name: "), self.facilityNameEntry)
        self.bottomLayout.addRow(QLabel("Location: "), self.facilityLocationEntry)
        self.bottomLayout.addRow(QLabel("Phone: "), self.facilityPhoneEntry)
        self.bottomLayout.addRow(QLabel("Email: "), self.facilityEmailEntry)
        self.bottomLayout.addRow(QLabel("Facility supervisor: "), self.facilitySupervisorEntry)
        self.bottomLayout.addRow(QLabel(""), self.attachPhotoBtn)
        self.bottomLayout.addRow(QLabel(""), self.addFacilityBtn)

        self.bottomFrame.setLayout(self.bottomLayout)

        # Add frames to main layout
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)


    def addFacility(self):
        name = self.facilityNameEntry.text()
        location = self.facilityLocationEntry.text()
        phone = self.facilityPhoneEntry.text()
        email = self.facilityEmailEntry.text()
        supervisor = self.facilitySupervisorEntry.text()



        if (name and location != ""):
            try:
                query = "INSERT INTO facilities (facility_name, facility_location, facility_phone, facility_email," \
                        "facility_supervisor) VALUES (?, ?, ?, ?, ?)"

                print("Before exec")
                print(name)
                print(location)
                print(phone)
                print(email)
                print(supervisor)

                db.cur.execute(query, (name, location, phone, email, supervisor))
                db.conn.commit()
                print("After exec")
                QMessageBox.information(self, "Info", "Facility has been added")
            except:
                QMessageBox.information(self, "Info", "Facility has not been added")
        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty")






