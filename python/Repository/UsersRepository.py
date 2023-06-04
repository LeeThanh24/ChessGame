from python.Config.mySQL import *
from python.Model.UsersModel import *


class UsersRepository:

    def __init__(self):
        self.connection = MySQL()

    def getAllUsers(self):
        cursor = self.connection.getCursor()
        query = "SELECT * FROM users"
        cursor.execute(query)
        result = cursor.fetchall()
        users = []
        for x in result:
            username = x[1]
            password = x[2]
            score = x[3]
            userModel = UsersModel(username, password, score)
            users.append(userModel)
        return users

    def insertUser(self, username='', password='', score=0):
        cursor = self.connection.getCursor()
        try:
            sql = "INSERT INTO users (username, password ,score) VALUES (%s, %s,%s )"
            val = (username, password, score)
            cursor.execute(sql, val)
            self.connection.db.commit()
            return True
        except:
            return False

    def findScoreByUsername(self,username ):
        users = self.getAllUsers()
        for user in users :
            if user.username==username :
                return user.score
        return 0

