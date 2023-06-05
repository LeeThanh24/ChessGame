from python.Repository.UsersRepository import *


class UsersService:

    def __init__(self):
        pass

    def checkLogin(self, username='', password=''):

        users = UsersRepository().getAllUsers()
        for x in users:
            if x.username == username and x.password == password:
                return True

        return False

    def findScoreByUsername(self,username ):

        return UsersRepository().findScoreByUsername(username)


    def updateScoreByUsername (self,username ,additiveScore ) :

        currScore = UsersRepository().getScoreByUsername(username)
        #print(f"currScore  : {currScore}")
        newScore = currScore+ additiveScore

        return UsersRepository().updateScoreByUsername(username,newScore)