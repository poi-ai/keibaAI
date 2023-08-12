from .jbis import Jbis
from .jra import Jra
from .keibago import Keibago
from .netkeiba import Netkeiba
from .rakuten import Rakuten

class Access():
    def __init__(self):
        self.jbis = Jbis()
        self.jra = Jra()
        self.keibago = Keibago()
        self.netkeiba = Netkeiba()
        self.rakuten = Rakuten()