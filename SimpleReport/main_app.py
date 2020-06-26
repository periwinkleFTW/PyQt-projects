import sys, os
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import sqlite3
from PIL import Image
import add_issue, display_issue
import add_person, display_person
import add_facility, display_facility
import backend

db = backend.Database("simplereport-data.db")


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("SimpleReport")
        # self.setWindowIcon(QIcon("assets/icons/logo-dark.png"))
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
        # self.tabs.addTab(self.tab4, "Statisticss")

    def widgets(self):
        # Tab 1 (Issues) widgets ###########################################################
        # Top layout (search issues) widgets
        self.searchIssuesText = QLabel("Search issues: ")
        self.searchIssuesEntry = QLineEdit()
        self.searchIssuesEntry.setPlaceholderText("Search issues..")
        self.searchIssuesBtn = QPushButton("Search")

        # Middle layout (list issues) widgets with radio buttons
        self.allIssuesRadioBtn = QRadioButton("All issues")
        self.ongoingIssuesRadioBtn = QRadioButton("Ongoing issues")
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
        self.issuesBottomRightLayout.addWidget(self.issuesBottomRightGroupBoxFiller, 75)
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
        self.peopleBottomRightLayout.addWidget(self.peopleBottomRightGroupBoxFiller, 75)
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
        self.facilitiesBottomRightLayout.addWidget(self.facilitiesBottomRightGroupBoxFiller, 75)
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
            for column_number, data in enumerate(row_data):
                self.issuesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.issuesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.issuesTable.setSelectionBehavior(QTableView.SelectRows)

    def displayPeople(self):
        for i in reversed(range(self.peopleTable.rowCount())):
            self.peopleTable.removeRow(i)

        cur = db.cur
        people = cur.execute("SELECT * FROM people")

        for row_data in people:
            row_number = self.peopleTable.rowCount()
            self.peopleTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.peopleTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.peopleTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.peopleTable.setSelectionBehavior(QTableView.SelectRows)

    def displayFacilities(self):
        for i in reversed(range(self.facilitiesTable.rowCount())):
            self.facilitiesTable.removeRow(i)

        cur = db.cur
        facilities = cur.execute("SELECT * FROM facilities")

        for row_data in facilities:
            row_number = self.facilitiesTable.rowCount()
            self.facilitiesTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.facilitiesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.facilitiesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.facilitiesTable.setSelectionBehavior(QTableView.SelectRows)

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
                    "OR issue_inspector LIKE ?" \
                    "OR issue_theme LIKE ?" \
                    "OR issue_facility LIKE ?" \
                    "OR issue_fac_supervisor LIKE ?" \
                    "OR issue_spec_loc LIKE ?" \
                    "OR issue_insp_dept LIKE ?" \
                    "OR issue_insp_contr LIKE ?" \
                    "OR issue_insp_subcontr LIKE ?" \
                    "OR issue_dealine LIKE ?"
            results = db.cur.execute(query, ('%'+value+'%', '%'+value+'%', '%'+value+'%', '%'+value+'%',
                                             '%'+value+'%', '%'+value+'%', '%'+value+'%', '%'+value+'%',
                                             '%'+value+'%', '%'+value+'%', '%'+value+'%', '%'+value+'%',
                                             '%'+value+'%', '%'+value+'%', )).fetchall()
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
        #global issueId
        row = self.issuesTable.currentRow()
        issueId = int(self.issuesTable.item(row, 0).text())

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




# class DisplayIssue(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("View issue")
#         self.setWindowIcon(QIcon("assets/icons/logo-dark.png"))
#         self.setGeometry(450, 150, 750, 650)
#         self.UI()
#         self.show()
#
#     def UI(self):
#         self.issueDetails()
#         self.widgets()
#         self.layouts()
#
#     def issueDetails(self):
#         global issueId
#         # row = self.issuesTable.currentRow()
#         # issueId = self.issuesTable.item(row, 0).text()
#
#         query = "SELECT * FROM issues WHERE issue_id=?"
#
#         cur = db.cur
#         issue = cur.execute(query, (issueId,)).fetchone()
#
#         self.id = issue[0]
#         self.date = issue[1]
#         self.priority = issue[2]
#         self.observer = issue[3]
#         self.revTeam = issue[4]
#         self.inspectorName = issue[5]
#         self.theme = issue[6]
#         self.facility = issue[7]
#         self.facilitySupervisor = issue[8]
#         self.specLocation = issue[9]
#         self.inspectedDept = issue[10]
#         self.inspectedContr = issue[11]
#         self.inspectedSubcontr = issue[12]
#         self.deadline = issue[13]
#         self.status = issue[14]
#
#     def widgets(self):
#         # Top layout widgets
#         self.issueImg = QLabel()
#         self.img = QPixmap('assets/icons/logo-dark.png')
#         self.issueImg.setPixmap(self.img)
#         self.issueImg.setAlignment(Qt.AlignCenter)
#         self.titleText = QLabel("Display issue")
#         self.titleText.setAlignment(Qt.AlignCenter)
#         # Bottom layout widgets
#         self.idEntry = QLabel(str(self.id))
#         self.dateEntry = QLineEdit()
#         self.dateEntry.setText(self.date)
#         self.priorityEntry = QLineEdit()
#         self.priorityEntry.setText(self.priority)
#         self.observerEntry = QLineEdit()
#         self.observerEntry.setText(self.observer)
#         self.revTeamEntry = QLineEdit()
#         self.revTeamEntry.setText(self.revTeam)
#         self.inspectorNameEntry = QLineEdit()
#         self.inspectorNameEntry.setText(self.inspectorName)
#         self.themeEntry = QLineEdit()
#         self.themeEntry.setText(self.theme)
#         self.facilityEntry = QLineEdit()
#         self.facilityEntry.setText(self.facility)
#         self.facilitySupervisorEntry = QLineEdit()
#         self.facilitySupervisorEntry.setText(self.facilitySupervisor)
#         self.specLocationEntry = QLineEdit()
#         self.specLocationEntry.setText(self.specLocation)
#         self.inspectedDeptEntry = QLineEdit()
#         self.inspectedDeptEntry.setText(self.inspectedDept)
#         self.inspectedContrEntry = QLineEdit()
#         self.inspectedContrEntry.setText(self.inspectedContr)
#         self.inspectedSubcontrEntry = QLineEdit()
#         self.inspectedSubcontrEntry.setText(self.inspectedSubcontr)
#         self.deadlineEntry = QLineEdit()
#         self.deadlineEntry.setText(self.deadline)
#
#         statusList = ["Open", "Closed"]
#         self.statusEntry = QComboBox()
#         self.statusEntry.addItems(statusList)
#
#         self.updateBtn = QPushButton("Update")
#         self.deleteBtn = QPushButton("Delete")
#
#     def layouts(self):
#         self.mainLayout = QVBoxLayout()
#         self.topLayout = QVBoxLayout()
#         self.bottomLayout = QFormLayout()
#         self.topFrame = QFrame()
#         self.bottomFrame = QFrame()
#
#         # Add widgets
#         self.topLayout.addWidget(self.titleText)
#         self.topLayout.addWidget(self.issueImg)
#         self.topFrame.setLayout(self.topLayout)
#
#         self.bottomLayout.addRow("ID: ", self.idEntry)
#         self.bottomLayout.addRow("Date: ", self.dateEntry)
#         self.bottomLayout.addRow("Priority: ", self.priorityEntry)
#         self.bottomLayout.addRow("Observer: ", self.observerEntry)
#         self.bottomLayout.addRow("Revision Team: ", self.revTeamEntry)
#         self.bottomLayout.addRow("Inspector name: ", self.inspectorNameEntry)
#         self.bottomLayout.addRow("HSE theme: ", self.themeEntry)
#         self.bottomLayout.addRow("Facility: ", self.facilityEntry)
#         self.bottomLayout.addRow("Facility supervisor: ", self.facilitySupervisorEntry)
#         self.bottomLayout.addRow("Specific location: ", self.specLocationEntry)
#         self.bottomLayout.addRow("Inspected department: ", self.inspectedDeptEntry)
#         self.bottomLayout.addRow("Inspected contractor: ", self.inspectedContrEntry)
#         self.bottomLayout.addRow("Inspected subcontractor: ", self.inspectedSubcontrEntry)
#         self.bottomLayout.addRow("Deadline: ", self.deadlineEntry)
#         self.bottomLayout.addRow("Status: ", self.statusEntry)
#         self.bottomLayout.addRow("", self.updateBtn)
#         self.bottomLayout.addRow("", self.deleteBtn)
#         self.bottomFrame.setLayout(self.bottomLayout)
#
#         self.mainLayout.addWidget(self.topFrame)
#         self.mainLayout.addWidget(self.bottomFrame)
#
#         self.setLayout(self.mainLayout)


# class DisplayPerson(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("View person")
#         self.setWindowIcon(QIcon("assets/icons/logo-dark.png"))
#         self.setGeometry(450, 150, 750, 650)
#         self.UI()
#         self.show()
#
#     def UI(self):
#         self.personDetails()
#         self.widgets()
#         self.layouts()
#
#     def personDetails(self):
#         global personId
#
#         query = "SELECT * FROM people WHERE person_id=?"
#
#         cur = db.cur
#         person = cur.execute(query, (personId,)).fetchone()
#
#         self.id = person[0]
#         self.firstName = person[1]
#         self.lastName = person[2]
#         self.title = person[3]
#         self.phone = person[4]
#         self.email = person[5]
#         self.location = person[6]
#         self.emplType = person[7]
#
#     def widgets(self):
#         # Top layout widgets
#         self.personImg = QLabel()
#         self.img = QPixmap('assets/icons/logo-dark.png')
#         self.personImg.setPixmap(self.img)
#         self.personImg.setAlignment(Qt.AlignCenter)
#         self.titleText = QLabel("Display person")
#         self.titleText.setAlignment(Qt.AlignCenter)
#         # Bottom layout widgets
#         self.idEntry = QLabel(str(self.id))
#         self.firstNameEntry = QLineEdit()
#         self.firstNameEntry.setText(self.firstName)
#         self.lastNameEntry = QLineEdit()
#         self.lastNameEntry.setText(self.lastName)
#         self.titleEntry = QLineEdit()
#         self.titleEntry.setText(self.title)
#         self.phoneEntry = QLineEdit()
#         self.phoneEntry.setText(self.phone)
#         self.emailEntry = QLineEdit()
#         self.emailEntry.setText(self.email)
#         self.locationEntry = QLineEdit()
#         self.locationEntry.setText(self.location)
#         self.emplTypeEntry = QLineEdit()
#         self.emplTypeEntry.setText(self.emplType)
#         self.updateBtn = QPushButton("Update")
#         self.deleteBtn = QPushButton("Delete")
#
#     def layouts(self):
#         self.mainLayout = QVBoxLayout()
#         self.topLayout = QVBoxLayout()
#         self.bottomLayout = QFormLayout()
#         self.topFrame = QFrame()
#         self.bottomFrame = QFrame()
#
#         # Add widgets
#         self.topLayout.addWidget(self.titleText)
#         self.topLayout.addWidget(self.personImg)
#         self.topFrame.setLayout(self.topLayout)
#
#         self.bottomLayout.addRow("ID: ", self.idEntry)
#         self.bottomLayout.addRow("First name: ", self.firstNameEntry)
#         self.bottomLayout.addRow("Last name: ", self.lastNameEntry)
#         self.bottomLayout.addRow("Title: ", self.titleEntry)
#         self.bottomLayout.addRow("Phone: ", self.phoneEntry)
#         self.bottomLayout.addRow("Email: ", self.emailEntry)
#         self.bottomLayout.addRow("Location: ", self.locationEntry)
#         self.bottomLayout.addRow("Employment type: ", self.emplTypeEntry)
#         self.bottomLayout.addRow("", self.updateBtn)
#         self.bottomLayout.addRow("", self.deleteBtn)
#         self.bottomFrame.setLayout(self.bottomLayout)
#
#         self.mainLayout.addWidget(self.topFrame)
#         self.mainLayout.addWidget(self.bottomFrame)
#
#         self.setLayout(self.mainLayout)


# class DisplayFacility(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("View facility")
#         self.setWindowIcon(QIcon("assets/icons/logo-dark.png"))
#         self.setGeometry(450, 150, 750, 650)
#         self.UI()
#         self.show()
#
#     def UI(self):
#         self.facilityDetails()
#         self.widgets()
#         self.layouts()
#
#     def facilityDetails(self):
#         global facilityId
#
#         query = "SELECT * FROM facilities WHERE facility_id=?"
#
#         cur = db.cur
#         facility = cur.execute(query, (facilityId,)).fetchone()
#
#         self.id = facility[0]
#         self.name = facility[1]
#         self.location = facility[2]
#         self.phone = facility[3]
#         self.email = facility[4]
#         self.supervisor = facility[5]
#
#     def widgets(self):
#         # Top layout widgets
#         self.facilityImg = QLabel()
#         self.img = QPixmap('assets/icons/logo-dark.png')
#         self.facilityImg.setPixmap(self.img)
#         self.facilityImg.setAlignment(Qt.AlignCenter)
#         self.titleText = QLabel("Display facility")
#         self.titleText.setAlignment(Qt.AlignCenter)
#         # Bottom layout widgets
#         self.idEntry = QLabel(str(self.id))
#         self.nameEntry = QLineEdit()
#         self.nameEntry.setText(self.name)
#         self.locationEntry = QLineEdit()
#         self.locationEntry.setText(self.location)
#         self.phoneEntry = QLineEdit()
#         self.phoneEntry.setText(self.phone)
#         self.emailEntry = QLineEdit()
#         self.emailEntry.setText(self.email)
#         self.supervisorEntry = QLineEdit()
#         self.supervisorEntry.setText(self.supervisor)
#         self.updateBtn = QPushButton("Update")
#         self.deleteBtn = QPushButton("Delete")
#
#     def layouts(self):
#         self.mainLayout = QVBoxLayout()
#         self.topLayout = QVBoxLayout()
#         self.bottomLayout = QFormLayout()
#         self.topFrame = QFrame()
#         self.bottomFrame = QFrame()
#
#         # Add widgets
#         self.topLayout.addWidget(self.titleText)
#         self.topLayout.addWidget(self.facilityImg)
#         self.topFrame.setLayout(self.topLayout)
#
#         self.bottomLayout.addRow("ID: ", self.idEntry)
#         self.bottomLayout.addRow("First name: ", self.nameEntry)
#         self.bottomLayout.addRow("Last name: ", self.locationEntry)
#         self.bottomLayout.addRow("Title: ", self.phoneEntry)
#         self.bottomLayout.addRow("Phone: ", self.emailEntry)
#         self.bottomLayout.addRow("Email: ", self.supervisorEntry)
#         self.bottomLayout.addRow("", self.updateBtn)
#         self.bottomLayout.addRow("", self.deleteBtn)
#         self.bottomFrame.setLayout(self.bottomLayout)
#
#         self.mainLayout.addWidget(self.topFrame)
#         self.mainLayout.addWidget(self.bottomFrame)
#
#         self.setLayout(self.mainLayout)


def main():
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
