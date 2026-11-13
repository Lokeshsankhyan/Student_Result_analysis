import sqlite3
from pathlib import Path

class Database:
    def __init__(self, db_name="students.db"):
        self.connection = sqlite3.connect(Path(__file__).with_name(db_name))
        self.connection.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                uid TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                python INTEGER NOT NULL,
                daa INTEGER NOT NULL,
                dbms INTEGER NOT NULL,
                java INTEGER NOT NULL,
                os INTEGER NOT NULL,
                total INTEGER NOT NULL,
                percentage REAL NOT NULL,
                grade TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def _to_dict(self, row):
        return dict(row) if row else None

    def add_student(self, data):
        self.connection.execute("""
            INSERT INTO students
            (uid, name, python, daa, dbms, java, os, total, percentage, grade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        self.connection.commit()

    def update_student(self, old_uid, data):
        new_uid = data[0]
        self.connection.execute("""
            UPDATE students SET uid=?, name=?, python=?, daa=?, dbms=?,
            java=?, os=?, total=?, percentage=?, grade=? WHERE uid=?
        """, (*data, old_uid))
        self.connection.commit()

    def delete_student(self, uid):
        self.connection.execute("DELETE FROM students WHERE uid=?", (uid,))
        self.connection.commit()

    def get_all_students(self):
        rows = self.connection.execute("SELECT * FROM students").fetchall()
        return [dict(row) for row in rows]

    def get_student(self, uid):
        row = self.connection.execute("SELECT * FROM students WHERE uid=?", (uid,)).fetchone()
        return self._to_dict(row)

    def close(self):
        self.connection.close()
