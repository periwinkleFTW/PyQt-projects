import sqlite3
from sqlite3 import Error

import pandas


class Database:
    def __init__(self, db):
        self.conn = self.create_connection(db)
        self.cur = self.conn.cursor()

        self.sqlCreatePeopleTable = "CREATE TABLE IF NOT EXISTS people (" \
                                    "person_id TEXT PRIMARY KEY UNIQUE NOT NULL," \
                                    "person_first_name TEXT NOT NULL," \
                                    "person_last_name TEXT NOT NULL," \
                                    "person_title TEXT," \
                                    "person_phone TEXT," \
                                    "person_email TEXT UNIQUE NOT NULL," \
                                    "person_location TEXT," \
                                    "person_empl_type TEXT" \
                                    ")"
        self.sqlCreateFacilitiesTable = "CREATE TABLE IF NOT EXISTS facilities (" \
                                        "facility_id TEXT PRIMARY KEY UNIQUE NOT NULL," \
                                        "facility_name TEXT," \
                                        "facility_location TEXT," \
                                        "facility_phone TEXT NOT NULL," \
                                        "facility_email TEXT NOT NULL," \
                                        "facility_supervisor TEXT NOT NULL," \
                                        "FOREIGN KEY (facility_supervisor) REFERENCES people (person_id)" \
                                        ")"
        self.sqlCreateIssuesTable = "CREATE TABLE IF NOT EXISTS issues (" \
                                    "id SERIAL PRIMARY KEY UNIQUE NOT NULL," \
                                    "issue_id TEXT UNIQUE NOT NULL," \
                                    "issue_date TEXT NOT NULL," \
                                    "issue_priority TEXT NOT NULL," \
                                    "issue_observer TEXT NOT NULL," \
                                    "issue_team TEXT," \
                                    "issue_inspector TEXT NOT NULL," \
                                    "issue_theme TEXT NOT NULL," \
                                    "issue_facility TEXT NOT NULL," \
                                    "issue_fac_supervisor TEXT NOT NULL," \
                                    "issue_spec_loc TEXT," \
                                    "issue_insp_dept TEXT," \
                                    "issue_insp_contr TEXT," \
                                    "issue_insp_subcontr TEXT," \
                                    "issue_deadline TEXT NOT NULL," \
                                    "FOREIGN KEY (issue_observer) REFERENCES people (person_id)," \
                                    "FOREIGN KEY (issue_facility) REFERENCES facilities (facility_id)," \
                                    "FOREIGN KEY (issue_fac_supervisor) REFERENCES facilities (facility_supervisor)," \
                                    "FOREIGN KEY (issue_insp_contr) REFERENCES people (person_id)," \
                                    "FOREIGN KEY (issue_insp_subcontr) REFERENCES people (person_id)" \
                                    ")"

        if self.conn is not None:
            self.create_table(self.conn, self.sqlCreatePeopleTable)
            self.create_table(self.conn, self.sqlCreateFacilitiesTable)
            self.create_table(self.conn, self.sqlCreateIssuesTable)
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



