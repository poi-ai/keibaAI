from .past import Past
from .present import Present

class Execute():
    def __init__(self):
        self.past = Past()
        self.present = Present()