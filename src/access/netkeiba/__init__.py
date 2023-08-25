from .nar import Nar
from .jra import Jra

class Netkeiba():
    def __init__(self):
        self.jra = Jra()
        self.nar = Nar()
