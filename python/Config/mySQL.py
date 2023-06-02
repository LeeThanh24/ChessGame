import mysql.connector


class MySQL:
    def __init__(self):
        self.db = mysql.connector.connect(user='root', password='1234', host='localhost', database='Chess')

    def getCursor(self):
        return self.db.cursor()
