from .race_table import RaceTable
from .race_result import RaceResult
from .race_list import RaceList

class Nar():
    def __init__(self):
        self.race_table = RaceTable()
        self.race_result = RaceResult()
        self.race_list = RaceList()