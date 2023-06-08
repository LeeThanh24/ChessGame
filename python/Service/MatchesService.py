from python.Repository.MatchesRepository import *


class MatchesService:
    def __init__(self):
        pass

    def getAllMatches(self):
        return MatchesRepository().getAllMatches()

    def insertMatch (self,name = '',matchTime = '') :
        return MatchesRepository().insertMatch(name,matchTime)