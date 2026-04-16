import sqlite3


class Database:
    def __init__(self):

        self.connection = sqlite3.connect("src/db/qa_report.db")
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def getOwner(self):
        self.cursor.execute("SELECT * FROM Owner")
        owner = self.cursor.fetchall()
        return owner

    def getSettings(self):
        self.cursor.execute("SELECT * FROM settings_user")
        settings = self.cursor.fetchall()
        return settings

    def getProjects(self):
        self.cursor.execute("SELECT * FROM project")
        project = self.cursor.fetchall()
        return project

    def saveSettings(self, id_owner: int, id_project: int, department: str = ""):

        self.cursor.execute("SELECT COUNT(*) FROM settings_user")
        count = self.cursor.fetchone()[0]

        if count > 0:

            self.cursor.execute(
                """
                UPDATE settings_user 
                SET id_owner = ?, id_project = ?, department = ?
                WHERE rowid = (SELECT rowid FROM settings_user LIMIT 1)
            """,
                (id_owner, id_project, department),
            )
        else:
            self.cursor.execute(
                """
                INSERT INTO settings_user (id_owner, id_project, department)
                VALUES (?, ?, ?)
            """,
                (id_owner, id_project, department),
            )

        self.connection.commit()
