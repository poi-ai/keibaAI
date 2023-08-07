from .horse import Horse
from .race_list import RaceList
from .race_result import RaceResult
from .race_table import RaceTable
from .racing_calendar import RacingCalendar

class Jbis():
    def __init__(self):
        self.horse = Horse()
        self.race_list = RaceList()
        self.race_result = RaceResult()
        self.race_table = RaceTable()
        self.racing_calendar = RacingCalendar()