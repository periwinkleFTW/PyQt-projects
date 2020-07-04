import sys, datetime
import csv
import xlsxwriter

from PySide2.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QLabel, QLineEdit, QPushButton, \
    QRadioButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, \
    QGroupBox, QTableView, QAbstractItemView, QMessageBox, QHeaderView, QCheckBox, QFileDialog
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt

import add_issue, display_issue
import add_person, display_person
import add_facility, display_facility
import backend

db = backend.Database("sr-data.db")


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("SR")
        self.setWindowIcon(QIcon("assets/icons/logo-dark.png"))
        self.setGeometry(150, 150, 1470, 750)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.tabWidget()
        self.widgets()
        self.layouts()
        self.displayIssues()
        self.displayPeople()
        self.displayFacilities()

    def tabWidget(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()

        self.tabs.addTab(self.tab1, "Issues")
        self.tabs.addTab(self.tab2, "People")
        self.tabs.addTab(self.tab3, "Facilities")
        # self.tabs.addTab(self.tab4, "Statistics")

    def widgets(self):
        # Tab 1 (Issues) widgets ###########################################################
        # Top layout (search issues) widgets
        self.searchIssuesText = QLabel("Search issues: ")
        self.searchIssuesEntry = QLineEdit()
        self.searchIssuesEntry.setPlaceholderText("Search issues..")
        self.searchIssuesBtn = QPushButton("Search")
        self.searchIssuesBtn.clicked.connect(self.searchIssues)

        # Middle layout (list issues) widgets with radio buttons
        self.allIssuesRadioBtn = QRadioButton("All issues")
        self.ongoingIssuesRadioBtn = QRadioButton("Pending issues")
        self.lateIssuesRadioBtn = QRadioButton("Late issues")
        self.closedIssuesRadioBtn = QRadioButton("Closed issues")
        self.listIssuesBtn = QPushButton("List issues")
        self.listIssuesBtn.clicked.connect(self.listIssues)

        # Bottom layout widget
        # Table showing issues
        self.issuesTable = QTableWidget()
        self.issuesTable.setColumnCount(16)
        # self.issuesTable.setColumnHidden(0, True)
        self.issuesTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.issuesTable.setHorizontalHeaderItem(1, QTableWidgetItem("Date"))
        self.issuesTable.setHorizontalHeaderItem(2, QTableWidgetItem("Priority"))
        self.issuesTable.setHorizontalHeaderItem(3, QTableWidgetItem("Observer"))
        self.issuesTable.setHorizontalHeaderItem(4, QTableWidgetItem("Rev. Team"))
        self.issuesTable.setHorizontalHeaderItem(5, QTableWidgetItem("Inspection name"))
        self.issuesTable.setHorizontalHeaderItem(6, QTableWidgetItem("Theme"))
        self.issuesTable.setHorizontalHeaderItem(7, QTableWidgetItem("Facility"))
        self.issuesTable.setHorizontalHeaderItem(8, QTableWidgetItem("Facility Superv."))
        self.issuesTable.setHorizontalHeaderItem(9, QTableWidgetItem("Spec. Loc."))
        self.issuesTable.setHorizontalHeaderItem(10, QTableWidgetItem("Insp. Dept"))
        self.issuesTable.setHorizontalHeaderItem(11, QTableWidgetItem("Insp. Contr."))
        self.issuesTable.setHorizontalHeaderItem(12, QTableWidgetItem("Subcontr"))
        self.issuesTable.setHorizontalHeaderItem(13, QTableWidgetItem("Deadline"))
        self.issuesTable.setHorizontalHeaderItem(14, QTableWidgetItem("Status"))
        self.issuesTable.setHorizontalHeaderItem(15, QTableWidgetItem("Created on"))

        # Double clicking a row opens a window with issue details
        self.issuesTable.doubleClicked.connect(self.selectedIssue)

        # Buttons for actions on selected issues
        self.refreshIssuesBtn = QPushButton("Refresh")
        self.refreshIssuesBtn.clicked.connect(self.displayIssues)
        self.addIssue = QPushButton("Add issue")
        self.addIssue.clicked.connect(self.funcAddIssue)
        self.viewIssue = QPushButton("View/Edit issue")
        self.viewIssue.clicked.connect(self.selectedIssue)
        self.closeIssueBtn = QPushButton("Close issue")
        self.closeIssueBtn.clicked.connect(self.funcCloseIssue)
        self.deleteIssue = QPushButton("Delete issue")
        self.deleteIssue.clicked.connect(self.funcDeleteIssue)
        self.exportIssuesCSVBtn = QPushButton("Export CSV")
        self.exportIssuesCSVBtn.clicked.connect(self.funcIssuesToCSV)
        self.exportIssuesXLSXBtn = QPushButton("Export XLSX")
        self.exportIssuesXLSXBtn.clicked.connect(self.funcIssuestoXLSX)

        # Tab 2 (People) widgets ###########################################################
        # Top layout (search people) widgets
        self.searchPeopleText = QLabel("Search people: ")
        self.searchPeopleEntry = QLineEdit()
        self.searchPeopleEntry.setPlaceholderText("Search people..")
        self.searchPeopleBtn = QPushButton("Search")
        self.searchPeopleBtn.clicked.connect(self.searchPeople)

        # Middle layout (list people) widgets with radio buttons
        self.allPeopleRadioBtn = QRadioButton("All people")
        self.employeesPeopleRadioBtn = QRadioButton("Employees")
        self.contractorsPeopleRadioBtn = QRadioButton("Contractors")
        self.subcontractorsPeopleRadioBtn = QRadioButton("Subcontractors")
        self.listPeopleBtn = QPushButton("List people")
        self.listPeopleBtn.clicked.connect(self.listPeople)

        # Bottom layout widget, a table showing people
        self.peopleTable = QTableWidget()
        self.peopleTable.setColumnCount(8)
        # self.peopleTable.setColumnHidden(0, True)
        self.peopleTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.peopleTable.setHorizontalHeaderItem(1, QTableWidgetItem("First name"))
        self.peopleTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.peopleTable.setHorizontalHeaderItem(2, QTableWidgetItem("Last name"))
        self.peopleTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.peopleTable.setHorizontalHeaderItem(3, QTableWidgetItem("Title"))
        self.peopleTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.peopleTable.setHorizontalHeaderItem(4, QTableWidgetItem("Phone"))
        self.peopleTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.peopleTable.setHorizontalHeaderItem(5, QTableWidgetItem("Email"))
        self.peopleTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.peopleTable.setHorizontalHeaderItem(6, QTableWidgetItem("Location"))
        self.peopleTable.setHorizontalHeaderItem(7, QTableWidgetItem("Employment type"))

        # Double clicking a row opens a window with person details
        self.peopleTable.doubleClicked.connect(self.selectedPerson)

        # Buttons for actions on selected people
        self.refreshPeopleBtn = QPushButton("Refresh")
        self.refreshPeopleBtn.clicked.connect(self.displayPeople)
        self.addPerson = QPushButton("Add person")
        self.addPerson.clicked.connect(self.funcAddPerson)
        self.viewPerson = QPushButton("View/Edit person")
        self.viewPerson.clicked.connect(self.selectedPerson)
        self.deletePerson = QPushButton("Delete person")
        self.deletePerson.clicked.connect(self.funcDeletePerson)
        self.exportPeopleCSVBtn = QPushButton("Export CSV")
        self.exportPeopleCSVBtn.clicked.connect(self.funcPeopleToCSV)
        self.exportPeopleXLSXBtn = QPushButton("Export XLSX")
        self.exportPeopleXLSXBtn.clicked.connect(self.funcPeopleToXLSX)

        # Tab 3 (Facilities) widgets ###########################################################
        # Top layout (search facilities) widgets
        self.searchFacilitiesText = QLabel("Search facilities: ")
        self.searchFacilitesEntry = QLineEdit()
        self.searchFacilitesEntry.setPlaceholderText("Search facilities..")
        self.searchFacilitiesBtn = QPushButton("Search")
        self.searchFacilitiesBtn.clicked.connect(self.searchFacilities)

        # Middle layout (list people) widgets with radio buttons
        self.allFacilitiesRadioBtn = QRadioButton("All facilities")
        self.withOngoingIssuesFacilitiesRadioBtn = QRadioButton("With ongoing issues")
        self.withLateIssuesRadioBtn = QRadioButton("With late issues")
        self.listFacilitiesBtn = QPushButton("List facilities")

        # Bottom layout widget, a table showing people
        self.facilitiesTable = QTableWidget()
        self.facilitiesTable.setColumnCount(10)
        # self.peopleTable.setColumnHidden(0, True)
        self.facilitiesTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.facilitiesTable.setHorizontalHeaderItem(1, QTableWidgetItem("Name"))
        self.facilitiesTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.facilitiesTable.setHorizontalHeaderItem(2, QTableWidgetItem("Location"))
        self.facilitiesTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.facilitiesTable.setHorizontalHeaderItem(3, QTableWidgetItem("Phone"))
        self.facilitiesTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.facilitiesTable.setHorizontalHeaderItem(4, QTableWidgetItem("Email"))
        self.facilitiesTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.facilitiesTable.setHorizontalHeaderItem(5, QTableWidgetItem("Supervisor"))
        self.facilitiesTable.setHorizontalHeaderItem(6, QTableWidgetItem("Ongoing issues"))
        self.facilitiesTable.setHorizontalHeaderItem(7, QTableWidgetItem("Late issues"))
        self.facilitiesTable.setHorizontalHeaderItem(8, QTableWidgetItem("Total issues"))
        self.facilitiesTable.setHorizontalHeaderItem(9, QTableWidgetItem("Total inspections"))

        # Double clicking a row opens a window with person details
        self.facilitiesTable.doubleClicked.connect(self.selectedFacility)

        # Buttons for actions on selected facilities
        self.refreshFacilitiesBtn = QPushButton("Refresh")
        self.refreshFacilitiesBtn.clicked.connect(self.displayFacilities)
        self.addFacility = QPushButton("Add facility")
        self.addFacility.clicked.connect(self.funcAddFacility)
        self.viewFacility = QPushButton("View/Edit facility")
        self.viewFacility.clicked.connect(self.selectedFacility)
        self.deleteFacility = QPushButton("Delete facility")
        self.deleteFacility.clicked.connect(self.funcDeleteFacility)
        self.exportFacilitiesCSVBtn = QPushButton("Export CSV")
        self.exportFacilitiesCSVBtn.clicked.connect(self.funcFacilitiesToCSV)
        self.exportFacilitiesXSLXBtn = QPushButton("Export XLSX")
        self.exportFacilitiesXSLXBtn.clicked.connect(self.funcFacilitiesToXLSX)

        # Tab 4 (Statistics) widgets ###########################################################
        self.totalIssuesLabel = QLabel()
        self.totalPeopleLabel = QLabel()
        self.totalOngoingIssuesLabel = QLabel()
        self.totalLateIssuesLabel = QLabel()
        self.totalClosedIssues = QLabel()

    def layouts(self):
        # Tab 1 (Issues) layouts ###########################################################
        self.issuesMainLayout = QVBoxLayout()
        self.issuesMainTopLayout = QHBoxLayout()
        self.issuesMainMiddleLayout = QHBoxLayout()
        self.issuesMainBottomLayout = QHBoxLayout()
        self.issuesBottomRightLayout = QVBoxLayout()
        self.issuesBottomLeftLayout = QHBoxLayout()
        # Groupboxes allow customization using CSS-like syntax
        self.issuesTopGroupBox = QGroupBox("Search Box")
        self.issuesTopGroupBoxRightFiller = QGroupBox()
        self.issuesMiddleGroupBox = QGroupBox("List Box")
        self.issuesMiddleGroupBoxRightFiller = QGroupBox()
        self.issuesBottomGroupBox = QGroupBox()
        self.issuesBottomLeftGroupBox = QGroupBox("Issues")
        self.issuesBottomRightGroupBox = QGroupBox("Actions")
        self.issuesBottomRightGroupBoxFiller = QGroupBox()

        # Add widgets
        # Top layout (search box) widgets
        self.issuesMainTopLayout.addWidget(self.searchIssuesText, 10)
        self.issuesMainTopLayout.addWidget(self.searchIssuesEntry, 30)
        self.issuesMainTopLayout.addWidget(self.searchIssuesBtn, 10)
        self.issuesMainTopLayout.addWidget(self.issuesTopGroupBoxRightFiller, 50)
        self.issuesTopGroupBox.setLayout(self.issuesMainTopLayout)

        # Middle layout (list box) widgets
        self.issuesMainMiddleLayout.addWidget(self.allIssuesRadioBtn)
        self.issuesMainMiddleLayout.addWidget(self.ongoingIssuesRadioBtn)
        self.issuesMainMiddleLayout.addWidget(self.lateIssuesRadioBtn)
        self.issuesMainMiddleLayout.addWidget(self.closedIssuesRadioBtn)
        self.issuesMainMiddleLayout.addWidget(self.listIssuesBtn)
        self.issuesMainMiddleLayout.addWidget(self.issuesMiddleGroupBoxRightFiller, 65)
        self.issuesMiddleGroupBox.setLayout(self.issuesMainMiddleLayout)

        # Bottom layout (table with facilities) widgets
        # Bottom left layout with table
        self.issuesBottomLeftLayout.addWidget(self.issuesTable)
        self.issuesBottomLeftGroupBox.setLayout(self.issuesBottomLeftLayout)

        # Bottom right layout with buttons
        self.issuesBottomRightLayout.addWidget(self.refreshIssuesBtn, 5)
        self.issuesBottomRightLayout.addWidget(self.addIssue, 5)
        self.issuesBottomRightLayout.addWidget(self.viewIssue, 5)
        self.issuesBottomRightLayout.addWidget(self.closeIssueBtn, 5)
        self.issuesBottomRightLayout.addWidget(self.deleteIssue, 5)
        self.issuesBottomRightLayout.addWidget(self.exportIssuesCSVBtn, 5)
        self.issuesBottomRightLayout.addWidget(self.exportIssuesXLSXBtn, 5)
        self.issuesBottomRightLayout.addWidget(self.issuesBottomRightGroupBoxFiller, 65)
        self.issuesBottomRightGroupBox.setLayout(self.issuesBottomRightLayout)

        self.issuesMainBottomLayout.addWidget(self.issuesBottomLeftGroupBox, 90)
        self.issuesMainBottomLayout.addWidget(self.issuesBottomRightGroupBox, 10)

        self.issuesMainLayout.addWidget(self.issuesTopGroupBox, 10)
        self.issuesMainLayout.addWidget(self.issuesMiddleGroupBox, 10)
        self.issuesMainLayout.addLayout(self.issuesMainBottomLayout, 80)

        self.tab1.setLayout(self.issuesMainLayout)

        # Tab 2 (People) layouts ###########################################################
        self.peopleMainLayout = QVBoxLayout()
        self.peopleMainTopLayout = QHBoxLayout()
        self.peopleMainMiddleLayout = QHBoxLayout()
        self.peopleMainBottomLayout = QHBoxLayout()
        self.peopleBottomRightLayout = QVBoxLayout()
        self.peopleBottomLeftLayout = QHBoxLayout()
        # Groupboxes allows customization using CSS-like syntax
        self.peopleTopGroupBox = QGroupBox("Search Box")
        self.peopleTopGroupBoxRightFiller = QGroupBox()
        self.peopleMiddleGroupBox = QGroupBox("List Box")
        self.peopleMiddleGroupBoxRightFiller = QGroupBox()
        self.peopleBottomGroupBox = QGroupBox()
        self.peopleBottomLeftGroupBox = QGroupBox("People")
        self.peopleBottomRightGroupBox = QGroupBox("Actions")
        self.peopleBottomRightGroupBoxFiller = QGroupBox()

        # Top layout (search box) widgets
        self.peopleMainTopLayout.addWidget(self.searchPeopleText, 10)
        self.peopleMainTopLayout.addWidget(self.searchPeopleEntry, 30)
        self.peopleMainTopLayout.addWidget(self.searchPeopleBtn, 10)
        self.peopleMainTopLayout.addWidget(self.peopleTopGroupBoxRightFiller, 50)
        self.peopleTopGroupBox.setLayout(self.peopleMainTopLayout)

        # Middle layout (list box) widgets
        self.peopleMainMiddleLayout.addWidget(self.allPeopleRadioBtn)
        self.peopleMainMiddleLayout.addWidget(self.employeesPeopleRadioBtn)
        self.peopleMainMiddleLayout.addWidget(self.contractorsPeopleRadioBtn)
        self.peopleMainMiddleLayout.addWidget(self.subcontractorsPeopleRadioBtn)
        self.peopleMainMiddleLayout.addWidget(self.listPeopleBtn)
        self.peopleMainMiddleLayout.addWidget(self.peopleMiddleGroupBoxRightFiller, 65)
        self.peopleMiddleGroupBox.setLayout(self.peopleMainMiddleLayout)

        # Bottom layout (table with issues) widgets
        # Bottom left layout with table
        self.peopleBottomLeftLayout.addWidget(self.peopleTable)
        self.peopleBottomLeftGroupBox.setLayout(self.peopleBottomLeftLayout)

        # Bottom right layout with buttons
        self.peopleBottomRightLayout.addWidget(self.refreshPeopleBtn, 5)
        self.peopleBottomRightLayout.addWidget(self.addPerson, 5)
        self.peopleBottomRightLayout.addWidget(self.viewPerson, 5)
        self.peopleBottomRightLayout.addWidget(self.deletePerson, 5)
        self.peopleBottomRightLayout.addWidget(self.exportPeopleCSVBtn, 5)
        self.peopleBottomRightLayout.addWidget(self.exportPeopleXLSXBtn, 5)
        self.peopleBottomRightLayout.addWidget(self.peopleBottomRightGroupBoxFiller, 70)
        self.peopleBottomRightGroupBox.setLayout(self.peopleBottomRightLayout)

        self.peopleMainBottomLayout.addWidget(self.peopleBottomLeftGroupBox, 90)
        self.peopleMainBottomLayout.addWidget(self.peopleBottomRightGroupBox, 10)

        self.peopleMainLayout.addWidget(self.peopleTopGroupBox, 10)
        self.peopleMainLayout.addWidget(self.peopleMiddleGroupBox, 10)
        self.peopleMainLayout.addLayout(self.peopleMainBottomLayout, 80)

        self.tab2.setLayout(self.peopleMainLayout)

        # Tab 3 (Facilities) layouts ###########################################################
        self.facilitiesMainLayout = QVBoxLayout()
        self.facilitiesMainTopLayout = QHBoxLayout()
        self.facilitiesMainMiddleLayout = QHBoxLayout()
        self.facilitiesMainBottomLayout = QHBoxLayout()
        self.facilitiesBottomRightLayout = QVBoxLayout()
        self.facilitiesBottomLeftLayout = QHBoxLayout()
        # Groupboxes allows customization using CSS-like syntax
        self.facilitiesTopGroupBox = QGroupBox("Search Box")
        self.facilitiesTopGroupBoxRightFiller = QGroupBox()
        self.facilitiesMiddleGroupBox = QGroupBox("List Box")
        self.facilitiesMiddleGroupBoxRightFiller = QGroupBox()
        self.facilitiesBottomGroupBox = QGroupBox()
        self.facilitiesBottomLeftGroupBox = QGroupBox("Facilities")
        self.facilitiesBottomRightGroupBox = QGroupBox("Actions")
        self.facilitiesBottomRightGroupBoxFiller = QGroupBox()

        # Top layout (search box) widgets
        self.facilitiesMainTopLayout.addWidget(self.searchFacilitiesText, 10)
        self.facilitiesMainTopLayout.addWidget(self.searchFacilitesEntry, 30)
        self.facilitiesMainTopLayout.addWidget(self.searchFacilitiesBtn, 10)
        self.facilitiesMainTopLayout.addWidget(self.facilitiesTopGroupBoxRightFiller, 50)
        self.facilitiesTopGroupBox.setLayout(self.facilitiesMainTopLayout)

        # Middle layout (list box) widgets
        self.facilitiesMainMiddleLayout.addWidget(self.allFacilitiesRadioBtn)
        self.facilitiesMainMiddleLayout.addWidget(self.withOngoingIssuesFacilitiesRadioBtn)
        self.facilitiesMainMiddleLayout.addWidget(self.withLateIssuesRadioBtn)
        self.facilitiesMainMiddleLayout.addWidget(self.listFacilitiesBtn)
        self.facilitiesMainMiddleLayout.addWidget(self.facilitiesMiddleGroupBoxRightFiller, 65)
        self.facilitiesMiddleGroupBox.setLayout(self.facilitiesMainMiddleLayout)

        # Bottom layout (table with facilities) widgets
        # Bottom left layout with table
        self.facilitiesBottomLeftLayout.addWidget(self.facilitiesTable)
        self.facilitiesBottomLeftGroupBox.setLayout(self.facilitiesBottomLeftLayout)

        # Bottom right layout with buttons
        self.facilitiesBottomRightLayout.addWidget(self.refreshFacilitiesBtn, 5)
        self.facilitiesBottomRightLayout.addWidget(self.addFacility, 5)
        self.facilitiesBottomRightLayout.addWidget(self.viewFacility, 5)
        self.facilitiesBottomRightLayout.addWidget(self.deleteFacility, 5)
        self.facilitiesBottomRightLayout.addWidget(self.exportFacilitiesCSVBtn, 5)
        self.facilitiesBottomRightLayout.addWidget(self.exportFacilitiesXSLXBtn, 5)
        self.facilitiesBottomRightLayout.addWidget(self.facilitiesBottomRightGroupBoxFiller, 70)
        self.facilitiesBottomRightGroupBox.setLayout(self.facilitiesBottomRightLayout)

        self.facilitiesMainBottomLayout.addWidget(self.facilitiesBottomLeftGroupBox, 90)
        self.facilitiesMainBottomLayout.addWidget(self.facilitiesBottomRightGroupBox, 10)

        self.facilitiesMainLayout.addWidget(self.facilitiesTopGroupBox, 10)
        self.facilitiesMainLayout.addWidget(self.facilitiesMiddleGroupBox, 10)
        self.facilitiesMainLayout.addLayout(self.facilitiesMainBottomLayout, 80)

        self.tab3.setLayout(self.facilitiesMainLayout)

    def funcAddIssue(self):
        self.newIssue = add_issue.AddIssue(self)

    def funcAddPerson(self):
        self.newPerson = add_person.AddPerson(self)

    def funcAddFacility(self):
        self.newFacility = add_facility.AddFacility(self)

    # Populating tables
    def displayIssues(self):
        for i in reversed(range(self.issuesTable.rowCount())):
            self.issuesTable.removeRow(i)

        issues = db.cur.execute("SELECT * FROM issues")

        for row_data in issues:
            row_number = self.issuesTable.rowCount()
            self.issuesTable.insertRow(row_number)
            # Add checkboxes to the table
            qwidget = QWidget()
            checkbox = QCheckBox()
            checkbox.setCheckState(Qt.Unchecked)
            qhboxlayout = QHBoxLayout(qwidget)
            qhboxlayout.addWidget(checkbox)
            qhboxlayout.setAlignment(Qt.AlignRight)
            qhboxlayout.setContentsMargins(0, 0, 20, 0)
            self.issuesTable.setCellWidget(row_number, 0, qwidget)
            self.issuesTable.setItem(row_number, 1, QTableWidgetItem(str(row_number)))

            for column_number, data in enumerate(row_data):
                if column_number == 0:
                    self.issuesTable.setItem(row_number, column_number, QTableWidgetItem("ISS#" + str(data)))
                else:
                    self.issuesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.issuesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.issuesTable.setSelectionBehavior(QTableView.SelectRows)

    def funcIssuesCheckBox(self):
        checked_list = []
        for i in range(self.issuesTable.rowCount()):
            if self.issuesTable.cellWidget(i, 0).findChild(type(QCheckBox())).isChecked():
                item = self.issuesTable.item(i, 0).text()
                checked_list.append(item.lstrip("ISS#"))
        return checked_list

    def displayPeople(self):
        for i in reversed(range(self.peopleTable.rowCount())):
            self.peopleTable.removeRow(i)

        cur = db.cur
        people = cur.execute("SELECT * FROM people")

        for row_data in people:
            row_number = self.peopleTable.rowCount()
            self.peopleTable.insertRow(row_number)
            # Add checkboxes to the table
            qwidget = QWidget()
            checkbox = QCheckBox()
            checkbox.setCheckState(Qt.Unchecked)
            qhboxlayout = QHBoxLayout(qwidget)
            qhboxlayout.addWidget(checkbox)
            qhboxlayout.setAlignment(Qt.AlignRight)
            qhboxlayout.setContentsMargins(0, 0, 20, 0)
            self.peopleTable.setCellWidget(row_number, 0, qwidget)
            self.peopleTable.setItem(row_number, 1, QTableWidgetItem(str(row_number)))

            for column_number, data in enumerate(row_data):
                if column_number == 0:
                    self.peopleTable.setItem(row_number, column_number, QTableWidgetItem("PRN#" + str(data)))
                else:
                    self.peopleTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.peopleTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.peopleTable.setSelectionBehavior(QTableView.SelectRows)

    def funcPeopleCheckBox(self):
        checked_list = []
        for i in range(self.peopleTable.rowCount()):
            if self.peopleTable.cellWidget(i, 0).findChild(type(QCheckBox())).isChecked():
                item = self.peopleTable.item(i, 0).text()
                checked_list.append(item.lstrip("PRN#"))
        return checked_list

    def displayFacilities(self):
        for i in reversed(range(self.facilitiesTable.rowCount())):
            self.facilitiesTable.removeRow(i)

        cur = db.cur
        facilities = cur.execute("SELECT * FROM facilities")

        for row_data in facilities:
            row_number = self.facilitiesTable.rowCount()
            self.facilitiesTable.insertRow(row_number)
            # Add checkboxes to the table
            qwidget = QWidget()
            checkbox = QCheckBox()
            checkbox.setCheckState(Qt.Unchecked)
            qhboxlayout = QHBoxLayout(qwidget)
            qhboxlayout.addWidget(checkbox)
            qhboxlayout.setAlignment(Qt.AlignRight)
            qhboxlayout.setContentsMargins(0, 0, 20, 0)
            self.facilitiesTable.setCellWidget(row_number, 0, qwidget)
            self.facilitiesTable.setItem(row_number, 1, QTableWidgetItem(str(row_number)))

            for column_number, data in enumerate(row_data):
                if column_number == 0:
                    self.facilitiesTable.setItem(row_number, column_number, QTableWidgetItem("FCL#" + str(data)))
                else:
                    self.facilitiesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.facilitiesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.facilitiesTable.setSelectionBehavior(QTableView.SelectRows)

    def funcFacilitiesCheckBox(self):
        checked_list = []
        for i in range(self.facilitiesTable.rowCount()):
            if self.facilitiesTable.cellWidget(i, 0).findChild(type(QCheckBox())).isChecked():
                item = self.facilitiesTable.item(i, 0).text()
                checked_list.append(item.lstrip("FCL#"))
        return checked_list

    # Selected items
    def selectedIssue(self):
        self.displayIssue = display_issue.DisplayIssue(self)
        self.displayIssue.show()

    def selectedPerson(self):
        self.displayPerson = display_person.DisplayPerson(self)
        self.displayPerson.show()

    def selectedFacility(self):
        self.displayFacility = display_facility.DisplayFacility(self)
        self.displayFacility.show()

    # Search functions
    def searchIssues(self):
        value = self.searchIssuesEntry.text()
        if value == "":
            QMessageBox.information(self, "Warning", "Search string cannot be empty")
            self.displayIssues()
        else:
            # Erase search entry
            self.searchIssuesEntry.setText("")
            query = "SELECT * FROM issues WHERE " \
                    "issue_id LIKE ? " \
                    "OR issue_date LIKE ?" \
                    "OR issue_priority LIKE ?" \
                    "OR issue_observer LIKE ?" \
                    "OR issue_team LIKE ?" \
                    "OR issue_inspection LIKE ?" \
                    "OR issue_theme LIKE ?" \
                    "OR issue_facility LIKE ?" \
                    "OR issue_fac_supervisor LIKE ?" \
                    "OR issue_spec_loc LIKE ?" \
                    "OR issue_insp_dept LIKE ?" \
                    "OR issue_insp_contr LIKE ?" \
                    "OR issue_insp_subcontr LIKE ?" \
                    "OR issue_deadline LIKE ?"
            results = db.cur.execute(query, ('%' + value + '%', '%' + value + '%', '%' + value + '%', '%' + value + '%',
                                             '%' + value + '%', '%' + value + '%', '%' + value + '%', '%' + value + '%',
                                             '%' + value + '%', '%' + value + '%', '%' + value + '%', '%' + value + '%',
                                             '%' + value + '%', '%' + value + '%',)).fetchall()
            if results == []:
                QMessageBox.information(self, "Info", "Nothing was found")
                self.displayIssues()
            else:
                for i in reversed(range(self.issuesTable.rowCount())):
                    self.issuesTable.removeRow(i)

                for row_data in results:
                    row_number = self.issuesTable.rowCount()
                    self.issuesTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.issuesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def searchPeople(self):
        value = self.searchPeopleEntry.text()
        if value == "":
            QMessageBox.information(self, "Warning", "Search string cannot be empty")
            self.displayPeople()
        else:
            # Erase search entry
            self.searchPeopleEntry.setText("")
            query = "SELECT * FROM people WHERE " \
                    "person_id LIKE ? " \
                    "OR person_first_name LIKE ?" \
                    "OR person_last_name LIKE ?" \
                    "OR person_title LIKE ?" \
                    "OR person_phone LIKE ?" \
                    "OR person_email LIKE ?" \
                    "OR person_location LIKE ?" \
                    "OR person_empl_type LIKE ?"
            results = db.cur.execute(query, ('%' + value + '%', '%' + value + '%', '%' + value + '%',
                                             '%' + value + '%', '%' + value + '%', '%' + value + '%',
                                             '%' + value + '%', '%' + value + '%',)).fetchall()
            if results == []:
                QMessageBox.information(self, "Info", "Nothing was found")
                self.displayPeople()
            else:
                for i in reversed(range(self.peopleTable.rowCount())):
                    self.peopleTable.removeRow(i)

                for row_data in results:
                    row_number = self.peopleTable.rowCount()
                    self.peopleTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.peopleTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def searchFacilities(self):
        value = self.searchFacilitesEntry.text()
        if value == "":
            QMessageBox.information(self, "Warning", "Search string cannot be empty")
            self.displayFacilities()
        else:
            # Erase search entry
            self.searchFacilitesEntry.setText("")
            query = "SELECT * FROM facilities WHERE " \
                    "facility_id LIKE ? " \
                    "OR facility_name LIKE ?" \
                    "OR facility_location LIKE ?" \
                    "OR facility_phone LIKE ?" \
                    "OR facility_email LIKE ?" \
                    "OR facility_supervisor LIKE ?"
            results = db.cur.execute(query, ('%' + value + '%', '%' + value + '%', '%' + value + '%',
                                             '%' + value + '%', '%' + value + '%', '%' + value + '%')).fetchall()
            if results == []:
                QMessageBox.information(self, "Info", "Nothing was found")
                self.displayFacilities()
            else:
                for i in reversed(range(self.facilitiesTable.rowCount())):
                    self.facilitiesTable.removeRow(i)

                for row_data in results:
                    row_number = self.facilitiesTable.rowCount()
                    self.facilitiesTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.facilitiesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    # List functions
    def listIssues(self):
        if self.allIssuesRadioBtn.isChecked():
            self.displayIssues()
        elif self.ongoingIssuesRadioBtn.isChecked():
            query = "SELECT * FROM issues WHERE status='Open' " \
                    "AND issue_deadline > DATETIME('now')"
            issues = db.cur.execute(query).fetchall()

            for i in reversed(range(self.issuesTable.rowCount())):
                self.issuesTable.removeRow(i)

            for row_data in issues:
                row_number = self.issuesTable.rowCount()
                self.issuesTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.issuesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        elif self.lateIssuesRadioBtn.isChecked():
            query = "SELECT * FROM issues WHERE status='Open' AND issue_deadline < DATETIME('now')"
            issues = db.cur.execute(query).fetchall()

            for i in reversed(range(self.issuesTable.rowCount())):
                self.issuesTable.removeRow(i)

            for row_data in issues:
                row_number = self.issuesTable.rowCount()
                self.issuesTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.issuesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        elif self.closedIssuesRadioBtn.isChecked():
            query = "SELECT * FROM issues WHERE status='Closed'"
            issues = db.cur.execute(query).fetchall()

            for i in reversed(range(self.issuesTable.rowCount())):
                self.issuesTable.removeRow(i)

            for row_data in issues:
                row_number = self.issuesTable.rowCount()
                self.issuesTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.issuesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def listPeople(self):
        if self.allPeopleRadioBtn.isChecked():
            self.displayPeople()
        elif self.employeesPeopleRadioBtn.isChecked():
            query = "SELECT * FROM people WHERE person_empl_type = 'Employee'"
            people = db.cur.execute(query).fetchall()

            for i in reversed(range(self.peopleTable.rowCount())):
                self.peopleTable.removeRow(i)

            for row_data in people:
                row_number = self.peopleTable.rowCount()
                self.peopleTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.peopleTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        elif self.contractorsPeopleRadioBtn.isChecked():
            query = "SELECT * FROM people WHERE person_empl_type = 'Contractor'"
            people = db.cur.execute(query).fetchall()

            for i in reversed(range(self.peopleTable.rowCount())):
                self.peopleTable.removeRow(i)

            for row_data in people:
                row_number = self.peopleTable.rowCount()
                self.peopleTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.peopleTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        elif self.subcontractorsPeopleRadioBtn.isChecked():
            query = "SELECT * FROM people WHERE person_empl_type = 'Subcontractor'"
            people = db.cur.execute(query).fetchall()

            for i in reversed(range(self.peopleTable.rowCount())):
                self.peopleTable.removeRow(i)

            for row_data in people:
                row_number = self.peopleTable.rowCount()
                self.peopleTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.peopleTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def funcCloseIssue(self):
        row = self.issuesTable.currentRow()
        issueId = self.issuesTable.item(row, 0).text()
        issueId = issueId.lstrip("ISS#")

        print(issueId, type(issueId))

        try:
            statusQuery = "SELECT status FROM issues WHERE issue_id=?"
            currentStatus = db.cur.execute(statusQuery, (issueId,)).fetchone()
            print(currentStatus)

            if currentStatus[0] == "Open":
                query = "UPDATE issues SET status='Closed' WHERE issue_id=?"

                print("Before exec")
                db.cur.execute(query, (issueId,))
                print("Before commit")
                db.conn.commit()
                print("after commit")

                QMessageBox.information(self, "Info", "Issue closed successfully")
                self.displayIssues()
            else:
                QMessageBox.information(self, "Info", "Issue is already closed")

        except:
            QMessageBox.information(self, "Info", "Something went wrong")

    # Delete functions
    def funcDeleteIssue(self):
        row = self.issuesTable.currentRow()
        issueId = self.issuesTable.item(row, 0).text()
        issueId = issueId.lstrip("ISS#")

        mbox = QMessageBox.question(self, "Warning", "Are you sure you want to delete issue " + issueId + "?",
                                    QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)

        if (mbox == QMessageBox.Yes):
            try:
                query = "DELETE FROM issues WHERE issue_id = ?"

                db.cur.execute(query, (issueId,))
                db.conn.commit()

                QMessageBox.information(self, "Info", "Issue was deleted")
                self.displayIssues()
            except:
                QMessageBox.information(self, "Info", "No changes made")

        self.displayIssue.close()

    def funcDeletePerson(self):
        row = self.peopleTable.currentRow()
        personId = self.peopleTable.item(row, 0).text()
        personId = personId.lstrip("PRN#")

        mbox = QMessageBox.question(self, "Warning", "Are you sure you want to delete this person?",
                                    QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)

        if (mbox == QMessageBox.Yes):
            try:
                query = "DELETE FROM people WHERE person_id = ?"

                db.cur.execute(query, (personId,))
                db.conn.commit()

                QMessageBox.information(self, "Info", "Person was deleted")
                self.displayPeople()
            except:
                QMessageBox.information(self, "Info", "No changes made")

        self.displayPerson.close()

    def funcDeleteFacility(self):
        row = self.facilitiesTable.currentRow()
        facilityId = self.facilitiesTable.item(row, 0).text()
        facilityId = facilityId.lstrip("FCL#")

        mbox = QMessageBox.question(self, "Warning", "Are you sure you want to delete this facility?",
                                    QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)

        if (mbox == QMessageBox.Yes):
            try:
                query = "DELETE FROM facilities WHERE facility_id = ?"

                db.cur.execute(query, (facilityId,))
                db.conn.commit()

                QMessageBox.information(self, "Info", "Facility was deleted")
                self.displayFacilities()
            except:
                QMessageBox.information(self, "Info", "No changes made")

        self.displayFacility.close()

    # Export to CSV
    def funcIssuesToCSV(self):
        indices = self.funcIssuesCheckBox()
        # Check if there are any selected items
        if indices:
            try:
                date = datetime.datetime.now()

                # Get file location and add timestamp to when it was created to the filename
                fileName, _ = QFileDialog.getSaveFileName(
                    self, "Save as...", "~/exportIssCSV" + "{:%d%b%Y_%Hh%Mm}".format(date) + ".csv",
                    "CSV files (*.csv)")
                if fileName:
                    with open(fileName, "w") as csv_file:
                        csv_writer = csv.writer(csv_file, delimiter="|")
                        # Setting cursor on the correct table
                        db.cur.execute("SELECT * FROM issues")
                        # Get headers
                        csv_writer.writerow([i[0] for i in db.cur.description])
                        for index in indices:
                            query = "SELECT * FROM issues WHERE issue_id=?"
                            facility_record = db.cur.execute(query, (index,)).fetchone()
                            csv_writer.writerow(facility_record)

                    QMessageBox.information(self, "Info", "Data exported successfully into {}".format(fileName))
            except:
                QMessageBox.information(self, "Info", "Export failed")
        else:
            QMessageBox.information(
                self, "Info", "Nothing selected for export\nUse checkboxes to select issues to export")

    def funcPeopleToCSV(self):
        indices = self.funcPeopleCheckBox()
        # Check if there are any selected items
        if indices:
            try:
                date = datetime.datetime.now()

                # Get file location and add timestamp to when it was created to the filename
                fileName, _ = QFileDialog.getSaveFileName(
                    self, "Save as...", "~/exportPplCSV" + "{:%d%b%Y_%Hh%Mm}".format(date) + ".csv",
                    "CSV files (*.csv)")
                if fileName:
                    with open(fileName, "w") as csv_file:
                        csv_writer = csv.writer(csv_file, delimiter="|")
                        # The purpose of this statement is to set cursor to correct table, needs rework because inefficient
                        db.cur.execute("SELECT * FROM people")
                        # Get headers from the table
                        csv_writer.writerow([i[0] for i in db.cur.description])
                        for index in indices:
                            query = "SELECT * FROM people WHERE person_id=?"
                            person_record = db.cur.execute(query, (index,)).fetchone()
                            csv_writer.writerow(person_record)

                    QMessageBox.information(self, "Info", "Data exported successfully into {}".format(fileName))
            except:
                QMessageBox.information(self, "Info", "Export failed")
        else:
            QMessageBox.information(
                self, "Info", "Nothing selected for export\nUse checkboxes to select people to export")

    def funcFacilitiesToCSV(self):
        indices = self.funcFacilitiesCheckBox()
        # Check if there are any selected items
        if indices:
            try:
                date = datetime.datetime.now()

                # Get file location and add timestamp to when it was created to the filename
                fileName, _ = QFileDialog.getSaveFileName(
                    self, "Save as...", "~/exportFclCSV" + "{:%d%b%Y_%Hh%Mm}".format(date) + ".csv",
                    "CSV files (*.csv)")
                if fileName:
                    with open(fileName, "w") as csv_file:
                        csv_writer = csv.writer(csv_file, delimiter="|")
                        # Setting cursor on the correct table
                        db.cur.execute("SELECT * FROM facilities")
                        # Get headers
                        csv_writer.writerow([i[0] for i in db.cur.description])
                        for index in indices:
                            query = "SELECT * FROM facilities WHERE facility_id=?"
                            facility_record = db.cur.execute(query, (index,)).fetchone()
                            csv_writer.writerow(facility_record)

                    QMessageBox.information(self, "Info", "Data exported successfully into {}".format(fileName))
            except:
                QMessageBox.information(self, "Info", "Export failed")
        else:
            QMessageBox.information(
                self, "Info", "Nothing selected for export\nUse checkboxes to select facilities to export")

    # Export to XLSX functions
    def funcIssuestoXLSX(self):
        indices = self.funcIssuesCheckBox()

        if indices:
            try:
                date = datetime.datetime.now()

                # Get file location and add timestamp to when it was created to the filename
                fileName, _ = QFileDialog.getSaveFileName(
                    self, "Save as...", "~/exportIssXLSX" + "{:%d%b%Y_%Hh%Mm}".format(date) + ".xlsx",
                    "Excel files (*.xlsx)")
                if fileName:
                    db.cur.execute("SELECT * FROM issues")

                    workbook = xlsxwriter.Workbook(fileName)
                    worksheet = workbook.add_worksheet("Issues")

                    # Create header row
                    col = 0
                    for value in db.cur.description:
                        worksheet.write(0, col, value[0])
                        col += 1

                    # Write date to xlsx file
                    for index in range(len(indices)):
                        query = "SELECT * FROM issues WHERE issue_id=?"
                        issue_record = db.cur.execute(query, (indices[index],)).fetchone()

                        row = 1
                        for i, value in enumerate(issue_record):
                            worksheet.write(row, i, value)
                        row += 1

                    workbook.close()

                    QMessageBox.information(self, "Info", "Data exported successfully into {}".format(fileName))

            except:
                QMessageBox.information(self, "Info", "Export failed")
        else:
            QMessageBox.information(
                self, "Info", "Nothing selected for export\nUse checkboxes to select issues to export")

    def funcPeopleToXLSX(self):
        indices = self.funcPeopleCheckBox()

        if indices:
            try:
                date = datetime.datetime.now()

                # Get file location and add timestamp to when it was created to the filename
                fileName, _ = QFileDialog.getSaveFileName(
                    self, "Save as...", "~/exportPrnXLSX" + "{:%d%b%Y_%Hh%Mm}".format(date) + ".xlsx",
                    "Excel files (*.xlsx)")
                if fileName:
                    db.cur.execute("SELECT * FROM people")

                    workbook = xlsxwriter.Workbook(fileName)
                    worksheet = workbook.add_worksheet("People")

                    # Create header row
                    col = 0
                    for value in db.cur.description:
                        worksheet.write(0, col, value[0])
                        col += 1

                    # Write date to xlsx file
                    for index in range(len(indices)):
                        query = "SELECT * FROM people WHERE person_id=?"
                        person_record = db.cur.execute(query, (indices[index],)).fetchone()

                        row = 1
                        for i, value in enumerate(person_record):
                            worksheet.write(row, i, value)
                        row += 1

                    workbook.close()

                    QMessageBox.information(self, "Info", "Data exported successfully into {}".format(fileName))

            except:
                QMessageBox.information(self, "Info", "Export failed")
        else:
            QMessageBox.information(
                self, "Info", "Nothing selected for export\nUse checkboxes to select issues to export")


    def funcFacilitiesToXLSX(self):
        indices = self.funcFacilitiesCheckBox()

        if indices:
            try:
                date = datetime.datetime.now()

                # Get file location and add timestamp to when it was created to the filename
                fileName, _ = QFileDialog.getSaveFileName(
                    self, "Save as...", "~/exportFclXLSX" + "{:%d%b%Y_%Hh%Mm}".format(date) + ".xlsx",
                    "Excel files (*.xlsx)")
                if fileName:
                    db.cur.execute("SELECT * FROM facilities")

                    workbook = xlsxwriter.Workbook(fileName)
                    worksheet = workbook.add_worksheet("Facilities")

                    # Create header row
                    col = 0
                    for value in db.cur.description:
                        worksheet.write(0, col, value[0])
                        col += 1

                    # Write date to xlsx file
                    for index in range(len(indices)):
                        query = "SELECT * FROM facilities WHERE facility_id=?"
                        facility_record = db.cur.execute(query, (indices[index],)).fetchone()

                        row = 1
                        for i, value in enumerate(facility_record):
                            worksheet.write(row, i, value)
                        row += 1

                    workbook.close()

                    QMessageBox.information(self, "Info", "Data exported successfully into {}".format(fileName))

            except:
                QMessageBox.information(self, "Info", "Export failed")
        else:
            QMessageBox.information(
                self, "Info", "Nothing selected for export\nUse checkboxes to select issues to export")

    # def populateDummyData(self):
    #     queryIssues = "INSERT INTO issues (" \
    #                   "issue_date, issue_priority, issue_observer, issue_team," \
    #                   "issue_inspection, issue_theme, issue_facility, issue_fac_supervisor," \
    #                   "issue_spec_loc, issue_insp_dept, issue_insp_contr, issue_insp_subcontr," \
    #                   "issue_deadline, status, created_on, closed_on)" \
    #                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" \
    #
    #
    #     queryPeople = "INSERT INTO people (person_first_name, person_last_name, person_title, person_phone," \
    #                   "person_email, person_location, person_empl_type) VALUES (?, ?, ?, ?, ?, ?, ?)"
    #
    #     queryFacility = "INSERT INTO facilities (facility_name, facility_location, facility_phone, " \
    #                     "facility_email, facility_supervisor)" \
    #                     "VALUES (?, ?, ?, ?, ?)"
    #
    #     issue1 = ['2020-06-26 19:39', 'Low', 'John Doe', 'Team1',
    #               'Internal audit', 'General safety', 'Facility1',
    #               'Miranda Brown', 'North staircase', 'Mech Engineering',
    #               '', '', '2020-07-26 12:00', 'Open', '2020-06-30 19:39', '']
    #
    #     issue2 = ('2020-06-23 10:30', 'High', 'John Doe', 'Team1',
    #               'Safety inspection', 'General safety', 'Facility1',
    #               'Miranda Brown', 'North staircase', 'Mech Engineering',
    #               '', '', '2020-09-25 12:00', 'Open', '2020-06-24 14:25', '')
    #
    #     issue3 = ('2020-06-26 19:39', 'Critical', 'John Doe', 'Team1',
    #               'Investigation', 'General safety', 'Facility1',
    #               'Miranda Brown', 'North staircase', 'Mech Engineering',
    #               '', '', '2020-07-26 12:00', 'Closed', '2020-06-28 19:39', '')
    #
    #     person1 = ('John', 'Doe', 'Safety officer', '355-234-3234', 'johnd@gmail.com', 'Calgary', 'Employee')
    #     person2 = ('Miranda', 'Brown', 'Safety officer', '332-432-6564', 'mirandab@gmail.com', 'Calgary', 'Contractor')
    #     person3 = ('Philip J.', 'Fry', 'Delivery boy', '233-543-6432', 'fryme@gmail.com', 'New New York', 'Subcontractor')
    #
    #     facility1 = ('Refinery', 'Richmond', '255-323-5456', 'refinery1@company.ca', 'Miranda Brown')
    #     facility2 = ('Main office', 'Victoria', '778-544-9056', 'hq@company.ca', 'Tom Riddle')
    #     facility3 = ('Factory', 'Quebec', '656-323-6767', 'factory1@company.ca', 'John Wick')
    #
    #     print("Before queries")
    #     db.cur.execute(queryIssues, issue1)
    #     db.cur.execute(queryIssues, issue2)
    #     db.cur.execute(queryIssues, issue3)
    #     #
    #     db.cur.execute(queryPeople, person1)
    #     db.cur.execute(queryPeople, person2)
    #     db.cur.execute(queryPeople, person3)
    #     #
    #     db.cur.execute(queryFacility, facility1)
    #     db.cur.execute(queryFacility, facility2)
    #     db.cur.execute(queryFacility, facility3)


def main():
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
