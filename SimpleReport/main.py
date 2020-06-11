import sys, os
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import sqlite3
from PIL import Image

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SimpleReport")
        self.setWindowIcon(QIcon("assets/icons/logo-dark.png"))
        self.setGeometry(150, 150, 1470, 750)
        #self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.tabWidget()
        self.widgets()
        self.layouts()

    def tabWidget(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tabs.addTab(self.tab1, "Issues")
        self.tabs.addTab(self.tab2, "People")
        self.tabs.addTab(self.tab3, "Facilities")

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

        # Bottom layout widget, a table showing issues
        self.issuesTable = QTableWidget()
        self.issuesTable.setColumnCount(14)
        #self.issuesTable.setColumnHidden(0, True)
        self.issuesTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.issuesTable.setHorizontalHeaderItem(1, QTableWidgetItem("Date"))
        self.issuesTable.setHorizontalHeaderItem(2, QTableWidgetItem("Priority"))
        self.issuesTable.setHorizontalHeaderItem(3, QTableWidgetItem("Observer"))
        self.issuesTable.setHorizontalHeaderItem(4, QTableWidgetItem("Rev. Team"))
        self.issuesTable.setHorizontalHeaderItem(5, QTableWidgetItem("Insp. Name"))
        self.issuesTable.setHorizontalHeaderItem(6, QTableWidgetItem("Theme"))
        self.issuesTable.setHorizontalHeaderItem(7, QTableWidgetItem("Facility"))
        self.issuesTable.setHorizontalHeaderItem(8, QTableWidgetItem("Facility Superv."))
        self.issuesTable.setHorizontalHeaderItem(9, QTableWidgetItem("Spec. Loc."))
        self.issuesTable.setHorizontalHeaderItem(10, QTableWidgetItem("Insp. Dept"))
        self.issuesTable.setHorizontalHeaderItem(11, QTableWidgetItem("Insp. Contr."))
        self.issuesTable.setHorizontalHeaderItem(12, QTableWidgetItem("Subcontr"))
        self.issuesTable.setHorizontalHeaderItem(13, QTableWidgetItem("Deadline"))

        # Tab 2 (People) widgets ###########################################################
        # Top layout (search people) widgets
        self.searchPeopleText = QLabel("Search people: ")
        self.searchPeopleEntry = QLineEdit()
        self.searchPeopleEntry.setPlaceholderText("Search people..")
        self.searchPeopleBtn = QPushButton("Search")

        # Middle layout (list people) widgets with radio buttons
        self.allPeopleRadioBtn = QRadioButton("All people")
        self.employeesPeopleRadioBtn = QRadioButton("Employees")
        self.contractorsPeopleRadioBtn = QRadioButton("Contractors")
        self.subcontractorsPeopleRadioBtn = QRadioButton("Subcontractors")
        self.listPeopleBtn = QPushButton("List people")

        # Bottom layout widget, a table showing people
        self.peopleTable = QTableWidget()
        self.peopleTable.setColumnCount(9)
        #self.peopleTable.setColumnHidden(0, True)
        self.peopleTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.peopleTable.setHorizontalHeaderItem(1, QTableWidgetItem("Name"))
        self.peopleTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.peopleTable.setHorizontalHeaderItem(2, QTableWidgetItem("Title"))
        self.peopleTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.peopleTable.setHorizontalHeaderItem(3, QTableWidgetItem("Phone"))
        self.peopleTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.peopleTable.setHorizontalHeaderItem(4, QTableWidgetItem("Email"))
        self.peopleTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.peopleTable.setHorizontalHeaderItem(5, QTableWidgetItem("Location"))
        self.peopleTable.setHorizontalHeaderItem(6, QTableWidgetItem("Staff"))
        self.peopleTable.setHorizontalHeaderItem(7, QTableWidgetItem("Contractor"))
        self.peopleTable.setHorizontalHeaderItem(8, QTableWidgetItem("Subcontractor"))

        # Tab 3 (Facilities) widgets ###########################################################
        # Top layout (search facilities) widgets
        self.searchFacilitiesText = QLabel("Search facilities: ")
        self.searchFacilitesEntry = QLineEdit()
        self.searchFacilitesEntry.setPlaceholderText("Search facilities..")
        self.searchFacilitiesBtn = QPushButton("Search")

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

    def layouts(self):
        # Tab 1 (Issues) layouts ###########################################################
        self.issuesMainLayout = QVBoxLayout()
        self.issuesMainTopLayout = QHBoxLayout()
        self.issuesMainMiddleLayout = QHBoxLayout()
        self.issuesMainBottomLayout = QHBoxLayout()
        self.issuesTopGroupBox = QGroupBox("Search Box")
        self.issuesTopGroupBoxRightFiller = QGroupBox()
        self.issuesMiddleGroupBox = QGroupBox("List Box")
        self.issuesMiddleGroupBoxRightFiller = QGroupBox()
        self.issuesBottomGroupBox = QGroupBox("Issues")

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
        self.issuesMainBottomLayout.addWidget(self.issuesTable)
        self.issuesBottomGroupBox.setLayout(self.issuesMainBottomLayout)

        self.issuesMainLayout.addWidget(self.issuesTopGroupBox, 10)
        self.issuesMainLayout.addWidget(self.issuesMiddleGroupBox, 10)
        self.issuesMainLayout.addWidget(self.issuesBottomGroupBox, 80)
        self.tab1.setLayout(self.issuesMainLayout)

        # Tab 2 (People) layouts ###########################################################
        self.peopleMainLayout = QVBoxLayout()
        self.peopleMainTopLayout = QHBoxLayout()
        self.peopleMainMiddleLayout = QHBoxLayout()
        self.peopleMainBottomLayout = QHBoxLayout()
        self.peopleTopGroupBox = QGroupBox("Search Box")
        self.peopleTopGroupBoxRightFiller = QGroupBox()
        self.peopleMiddleGroupBox = QGroupBox("List Box")
        self.peopleMiddleGroupBoxRightFiller = QGroupBox()
        self.peopleBottomGroupBox = QGroupBox("People")

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
        self.peopleMainBottomLayout.addWidget(self.peopleTable)
        self.peopleBottomGroupBox.setLayout(self.peopleMainBottomLayout)

        self.peopleMainLayout.addWidget(self.peopleTopGroupBox, 10)
        self.peopleMainLayout.addWidget(self.peopleMiddleGroupBox, 10)
        self.peopleMainLayout.addWidget(self.peopleBottomGroupBox, 80)
        self.tab2.setLayout(self.peopleMainLayout)

        # Tab 3 (Facilities) layouts ###########################################################
        self.facilitiesMainLayout = QVBoxLayout()
        self.facilitiesMainTopLayout = QHBoxLayout()
        self.facilitiesMainMiddleLayout = QHBoxLayout()
        self.facilitiesMainBottomLayout = QHBoxLayout()
        self.facilitiesTopGroupBox = QGroupBox("Search Box")
        self.facilitiesTopGroupBoxRightFiller = QGroupBox()
        self.facilitiesMiddleGroupBox = QGroupBox("List Box")
        self.facilitiesMiddleGroupBoxRightFiller = QGroupBox()
        self.facilitiesBottomGroupBox = QGroupBox("Facilities")

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
        self.facilitiesMainBottomLayout.addWidget(self.facilitiesTable)
        self.facilitiesBottomGroupBox.setLayout(self.facilitiesMainBottomLayout)

        self.facilitiesMainLayout.addWidget(self.facilitiesTopGroupBox, 10)
        self.facilitiesMainLayout.addWidget(self.facilitiesMiddleGroupBox, 10)
        self.facilitiesMainLayout.addWidget(self.facilitiesBottomGroupBox, 80)
        self.tab3.setLayout(self.facilitiesMainLayout)



def main():
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()