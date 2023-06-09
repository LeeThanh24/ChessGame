from python.Config.mySQL import *
from python.Model.MatchesModel import MatchesModel
from python.Model.UsersModel import *


class MatchesRepository:

    def __init__(self):
        self.connection = MySQL()
        self.cursor= self.connection.getCursor()
    def getAllMatches(self):
        cursor = self.cursor
        query = "SELECT * FROM matches order by match_time"
        cursor.execute(query)
        result = cursor.fetchall()
        matches = []
        for x in result:
            matchesModel = MatchesModel(x[1],x[2])
            matches.append(matchesModel)
        return matches

    def insertMatch(self, name='', matchTime=''):
        cursor = self.connection.getCursor()

        try:
            sql = "INSERT INTO matches (name, match_time ) VALUES (%s, %s )"
            val = (name, matchTime)
            cursor.execute(sql, val)
            self.connection.db.commit()
            print("co vo insert match trong try")
            return True
        except Exception as e:
            print(e)
            return False

