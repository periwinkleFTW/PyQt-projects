import sys, os
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import sqlite3
from PIL import Image

# conn = sqlite3.connect("simplereport-data.db")
# cur = conn.cursor()

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
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

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
        self.dateEntry = QDateEdit()
        self.observerEntry = QComboBox()
        self.observerEntry.setEditable(True)
        self.revisionTeamEntry = QComboBox()
        self.revisionTeamEntry.setEditable(True)
        self.inspectionNameEntry = QComboBox()
        self.inspectionNameEntry.setEditable(True)
        self.observationThemeEntry = QComboBox()
        self.observationThemeEntry.setEditable(True)
        self.facilityEntry = QComboBox()
        self.facilityEntry.setEditable(True)
        self.facilitySupervisorEntry = QComboBox()
        self.facilitySupervisorEntry.setEditable(True)
        self.specificLocationEntry = QTextEdit()
        self.inspectedDepartmentEntry = QComboBox()
        self.inspectedDepartmentEntry.setEditable(True)
        self.inspectedContractorEntry = QComboBox()
        self.inspectedContractorEntry.setEditable(True)
        self.inspectedSubcontractorEntry = QComboBox()
        self.inspectedSubcontractorEntry.setEditable(True)

        # Bottom layout widgets
        self.observationTitleText = QLabel("Observation details")
        self.observationTitleText.setAlignment(Qt.AlignCenter)
        self.observationDetailsEntry = QTextEdit()
        self.targetDateEntry = QDateEdit()
        self.priorityEntry = QComboBox()
        self.priorityEntry.setEditable(True)
        self.personResponsibleEntry = QComboBox()
        self.personResponsibleEntry.setEditable(True)
        self.actionDescriptionEntry =QTextEdit()
        self.attachFilesBtn = QPushButton("Attach files")
        self.addActionBtn = QPushButton("Add action")

        self.rootCauseEntry = QComboBox()
        self.rootCauseEntry.setEditable(True)
        self.rootCauseDetailsEntry = QTextEdit()
        self.rootCauseActionPartyEntry = QComboBox()
        self.rootCauseActionPartyEntry.setEditable(True)
        self.addRootCauseBtn = QPushButton("Add root cause")

        self.submitObservationBtn = QPushButton("Submit observation")

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()

        # Put elements into frames for visual distinction
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()


        # Add widgets to top layout
        self.topLayout.addWidget(self.addIssueImg)
        self.topLayout.addWidget(self.titleText)

        self.topFrame.setLayout(self.topLayout)

        # Add widgets to middle layout
        self.bottomLayout.addRow(self.issueInfoTitleText)
        self.bottomLayout.addRow(QLabel("Inspection Date: "), self.dateEntry)
        self.bottomLayout.addRow(QLabel("Observer: "), self.observerEntry)
        self.bottomLayout.addRow(QLabel("Revision Team: "), self.revisionTeamEntry)
        self.bottomLayout.addRow(QLabel("Inspection Name: "), self.inspectionNameEntry)
        self.bottomLayout.addRow(QLabel("HSE Theme: "), self.observationThemeEntry)
        self.bottomLayout.addRow(QLabel("Facility: "), self.facilityEntry)
        self.bottomLayout.addRow(QLabel("Facility supervisor: "), self.facilitySupervisorEntry)
        self.bottomLayout.addRow(QLabel("Specific location: "), self.specificLocationEntry)
        self.bottomLayout.addRow(QLabel("Inspected department: "), self.inspectedDepartmentEntry)
        self.bottomLayout.addRow(QLabel("Inspected contractor: "), self.inspectedContractorEntry)
        self.bottomLayout.addRow(QLabel("Inspected subcontractor: "), self.inspectedSubcontractorEntry)

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

        # Make bottom frame scollable
        self.scroll.setWidget(self.bottomFrame)

        # Add frames to main layout
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.scroll)

        self.setLayout(self.mainLayout)


class DisplayIssue(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View issue")
        self.setWindowIcon(QIcon("assets/icons/logo-dark.png"))
        self.setGeometry(450, 150, 750, 650)
        self.UI()
        self.show()

    def UI(self):
        pass






