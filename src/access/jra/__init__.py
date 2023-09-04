from .odds import Odds
from .race_list import RaceList

class Jra():
    def __init__(self):
        self.odds = Odds()
        self.race_list = RaceList()