import sqlite3

conn = sqlite3.connect("employees.db")


conn.cursor("
    CREATE TABLE "employees" (
        "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
        "first_name"	TEXT NOT NULL,
        "last_name"	TEXT NOT NULL,
        "phone"	TEXT NOT NULL,
        "email"	TEXT NOT NULL UNIQUE
    );
")