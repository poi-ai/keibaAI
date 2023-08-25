from .race_table import RaceTable
from .race_result import RaceResult
from .racing_calendar import RacingCalendar
from .race_list import RaceList

class Jra():
    def __init__(self):
        self.race_table = RaceTable()
        self.race_result = RaceResult()
        self.racing_calendar = RacingCalendar()
        self.race_list = RaceList()