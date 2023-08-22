from .nar import Nar
from .jra import Jra
from .race_list import RaceList
from .racing_calendar import RacingCalendar

class Netkeiba():
    def __init__(self):
        self.jra = Jra()
        self.nar = Nar()
        self.race_list = RaceList()
        self.racing_calendar = RacingCalendar()