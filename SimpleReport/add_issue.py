import sys, os
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import sqlite3
from PIL import Image

conn = sqlite3.connect("simplereport-data.db")
cur = conn.cursor()

defaultImg = "assets/icons/logo-dark.png"

class AddIssue(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add issue")
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
        self.addIssueImg = QLabel()
        self.img = QPixmap('assets/icons/create-issue.png')
        self.addIssueImg.setPixmap(self.img)
        self.addIssueImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Add issue")
        self.titleText.setAlignment(Qt.AlignCenter)
        # Middle layout widgets
        self.issueInfoTitleText = QLabel("Issue info")
        self.issueInfoTitleText.setAlignment(Qt.AlignCenter)
        self.dateEntry = QLineEdit()
        self.observerEntry = QLineEdit()
        ############### test ############
        self.revisionTeamEntry = QComboBox()
        self.revisionTeamEntry.setEditable(True)
        ############## end test #########
        self.inspectionNameEntry = QLineEdit()
        self.observationThemeEntry = QLineEdit()
        self.facilityEntry = QLineEdit()
        self.facilitySupervisorEntry = QLineEdit()
        self.specificLocationEntry = QLineEdit()
        self.inspectedDepartmentEntry = QLineEdit()
        self.inspectedContractorEntry = QLineEdit()
        self.inspectedSubcontractorEntry = QLineEdit()

        # Bottom layout widgets
        self.observationTitleText = QLabel("Observation details")
        self.observationTitleText.setAlignment(Qt.AlignCenter)
        self.observationDetailsEntry = QTextEdit()
        self.targetDateEntry = QLineEdit()
        self.priorityEntry = QLineEdit()
        self.personResponsibleEntry = QLineEdit()
        self.actionDescriptionEntry =QTextEdit()
        self.attachFilesBtn = QPushButton("Attach files")
        self.addActionBtn = QPushButton("Add action")

        self.rootCauseEntry = QLineEdit()
        self.rootCauseDetailsEntry = QTextEdit()
        self.rootCauseActionPartyEntry = QLineEdit()
        self.addRootCauseBtn = QPushButton("Add root cause")

        self.submitObservationBtn = QPushButton("Submit observation")

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.middleLayout = QFormLayout()
        self.bottomLayout = QFormLayout()
        # Put elements into frames for visual distinction
        self.topFrame = QFrame()
        self.middleFrame = QFrame()
        self.bottomFrame = QFrame()

        # Add widgets to top layout
        self.topLayout.addWidget(self.addIssueImg)
        self.topLayout.addWidget(self.titleText)

        self.topFrame.setLayout(self.topLayout)

        # Add widgets to middle layout
        self.middleLayout.addRow(self.issueInfoTitleText)
        self.middleLayout.addRow(QLabel("Inspection Date: "), self.dateEntry)
        self.middleLayout.addRow(QLabel("Observer: "), self.observerEntry)
        self.middleLayout.addRow(QLabel("Revision Team: "), self.revisionTeamEntry)
        self.middleLayout.addRow(QLabel("Inspection Name: "), self.inspectionNameEntry)
        self.middleLayout.addRow(QLabel("HSE Theme: "), self.observationThemeEntry)
        self.middleLayout.addRow(QLabel("Facility: "), self.facilityEntry)
        self.middleLayout.addRow(QLabel("Facility supervisor: "), self.facilitySupervisorEntry)
        self.middleLayout.addRow(QLabel("Specific location: "), self.specificLocationEntry)
        self.middleLayout.addRow(QLabel("Inspected department: "), self.inspectedDepartmentEntry)
        self.middleLayout.addRow(QLabel("Inspected contractor: "), self.inspectedContractorEntry)
        self.middleLayout.addRow(QLabel("Inspected subcontractor: "), self.inspectedSubcontractorEntry)

        self.middleFrame.setLayout(self.middleLayout)

        # Add widgets to bottom layout
        self.bottomLayout.addRow(self.observationTitleText)
        self.bottomLayout.addRow(QLabel("Observation details: "), self.observationDetailsEntry)
        self.bottomLayout.addRow(QLabel("Target date: "), self.targetDateEntry)
        self.bottomLayout.addRow(QLabel("Priority: "), self.priorityEntry)
        self.bottomLayout.addRow(QLabel("Person responsible: "), self.personResponsibleEntry)
        self.bottomLayout.addRow(QLabel("Action description: "), self.actionDescriptionEntry)
        self.bottomLayout.addRow(QLabel(""), self.attachFilesBtn)
        self.bottomLayout.addRow(QLabel(""), self.addActionBtn)
        self.bottomLayout.addRow(QLabel("Root cause: "), self.rootCauseEntry)
        self.bottomLayout.addRow(QLabel("Root cause details: "), self.rootCauseDetailsEntry)
        self.bottomLayout.addRow(QLabel("Root cause action party: "), self.rootCauseActionPartyEntry)
        self.bottomLayout.addRow(QLabel(""), self.addRootCauseBtn)
        self.bottomLayout.addRow(QLabel(""), self.submitObservationBtn)

        self.bottomFrame.setLayout(self.bottomLayout)

        # Add frames to main layout
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.middleFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)









