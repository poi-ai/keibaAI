import os, sys
from .scraping import Scraping

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'common'))

from .scraping.access import Access
from .scraping.db import Db
from .scraping.entity import Entity
from .scraping.execute import Execute

class Api():
    def __init__(self):
        self.access = Access()
        self.db = Db()
        self.entity = Entity()
        self.execute = Execute()
