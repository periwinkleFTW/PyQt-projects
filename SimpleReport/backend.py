import sqlite3
from sqlite3 import Error


# import pandas


class Database:
    def __init__(self, db):
        self.conn = self.create_connection(db)
        self.cur = self.conn.cursor()

        self.sqlCreatePeopleTable = "CREATE TABLE IF NOT EXISTS people (" \
                                    "person_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                                    "person_first_name TEXT," \
                                    "person_last_name TEXT," \
                                    "person_title TEXT," \
                                    "person_phone TEXT," \
                                    "person_email TEXT," \
                                    "person_location TEXT," \
                                    "person_empl_type TEXT" \
                                    ")"
        self.sqlCreateFacilitiesTable = "CREATE TABLE IF NOT EXISTS facilities (" \
                                        "facility_id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                                        "facility_name TEXT, " \
                                        "facility_location TEXT, " \
                                        "facility_phone TEXT NOT NULL, " \
                                        "facility_email TEXT NOT NULL, " \
                                        "facility_supervisor TEXT NOT NULL" \
                                        ")"
        self.sqlCreateIssuesTable = "CREATE TABLE IF NOT EXISTS issues (" \
                                    "issue_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                                    "issue_date TEXT," \
                                    "issue_priority TEXT," \
                                    "issue_observer TEXT," \
                                    "issue_team TEXT," \
                                    "issue_inspection TEXT," \
                                    "issue_theme TEXT," \
                                    "issue_facility TEXT," \
                                    "issue_fac_supervisor TEXT," \
                                    "issue_spec_loc TEXT," \
                                    "issue_insp_dept TEXT," \
                                    "issue_insp_contr TEXT," \
                                    "issue_insp_subcontr TEXT," \
                                    "issue_deadline DATETIME, " \
                                    "status TEXT DEFAULT 'Open', " \
                                    "created_on DATETIME, " \
                                    "closed_on DATETIME" \
                                    ")"

        if self.conn is not None:
            self.create_table(self.conn, self.sqlCreateIssuesTable)
            self.create_table(self.conn, self.sqlCreatePeopleTable)
            self.create_table(self.conn, self.sqlCreateFacilitiesTable)

        else:
            print("Error! Cannot establish database connection")

        #######################################################################
        # This block is used for populating db with dummy data from csv
        # Column names should match those in the table
        # *******************************
        # df1 = pandas.read_csv("data/person-data.csv", sep="|",)
        # df1.to_sql('people', self.conn, if_exists='append', index=False)
        # df2 = pandas.read_csv("data/facility-data.csv", sep="|")
        # df2.to_sql('facilities', self.conn, if_exists='append', index=False)
        #######################################################################

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn

    def create_table(self, conn, create_table_sql):
        try:
            cur = conn.cursor()
            cur.execute(create_table_sql)
        except Error as e:
            print(e)

    # def populateDummyData(self):
    #     queryIssues = "INSERT INTO issues (" \
    #                   "issue_date, issue_priority, issue_observer, issue_team," \
    #                   "issue_inspection, issue_theme, issue_facility, issue_fac_supervisor," \
    #                   "issue_spec_loc, issue_insp_dept, issue_insp_contr, issue_insp_subcontr," \
    #                   "issue_deadline, status, created_on, closed_on)" \
    #                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" \


        # queryPeople = "INSERT INTO people (person_first_name, person_last_name, person_title, person_phone," \
        #               "person_email, person_location, person_empl_type) VALUES (?, ?, ?, ?, ?, ?, ?)"
        #
        # queryFacility = "INSERT INTO facilities (facility_name, facility_location, facility_phone, " \
        #                 "facility_email, facility_supervisor)" \
        #                 "VALUES (?, ?, ?, ?, ?)"
        #
        # issue1 = ['2020-06-26 19:39', 'Low', 'John Doe', 'Team1',
        #           'Internal audit', 'General safety', 'Facility1',
        #           'Miranda Brown', 'North staircase', 'Mech Engineering',
        #           '', '', '2020-07-26 12:00', 'Open', '2020-06-30 19:39', '']
        #
        # issue2 = ('2020-06-23 10:30', 'High', 'John Doe', 'Team1',
        #           'Internal audit', 'General safety', 'Facility1',
        #           'Miranda Brown', 'North staircase', 'Mech Engineering',
        #           '', '', '2020-09-25 12:00', 'Open', '2020-06-24 14:25', '')
        #
        # issue3 = ('2020-06-26 19:39', 'Critical', 'John Doe', 'Team1',
        #           'Internal audit', 'General safety', 'Facility1',
        #           'Miranda Brown', 'North staircase', 'Mech Engineering',
        #           '', '', '2020-07-26 12:00', 'Closed', '2020-06-28 19:39', '')
        #
        # person1 = ('John', 'Doe', 'Safety officer', '355-234-3234', 'johnd@gmail.com', 'Calgary', 'Employee')
        # person2 = ('Miranda', 'Brown', 'Safety officer', '332-432-6564', 'mirandab@gmail.com', 'Calgary', 'Contractor')
        # person3 = ('Philip J.', 'Fry', 'Delivery boy', '233-543-6432', 'fryme@gmail.com', 'New New York', 'Subcontractor')
        #
        # facility1 = ('Refinery', 'Richmond', '255-323-5456', 'refinery1@company.ca', 'Miranda Brown')
        # facility2 = ('Main office', 'Victoria', '778-544-9056', 'hq@company.ca', 'Tom Riddle')
        # facility3 = ('Factory', 'Quebec', '656-323-6767', 'factory1@company.ca', 'John Wick')
        #
        # print("Before queries")
        # self.cur.execute(queryIssues, issue1)
        # self.cur.execute(queryIssues, issue2)
        # self.cur.execute(queryIssues, issue3)
        #
        # self.cur.execute(queryPeople, person1)
        # self.cur.execute(queryPeople, person2)
        # self.cur.execute(queryPeople, person3)
        #
        # self.cur.execute(queryFacility, facility1)
        # self.cur.execute(queryFacility, facility2)
        # self.cur.execute(queryFacility, facility3)
