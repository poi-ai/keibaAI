from .race_table import RaceTable
from .race_result import RaceResult

class Jra():
    def __init__(self):
        self.race_table = RaceTable()
        self.race_result = RaceResult()