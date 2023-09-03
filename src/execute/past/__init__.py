from .race_data import RaceData
from .race_result import RaceResult

class Past():
    def __init__(self):
        self.race_data = RaceData()
        self.race_result = RaceResult()