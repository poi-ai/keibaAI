from .access import Access
from .db import Db
from .entity import Entity
from .execute import Execute

class Scraping():
    def __init__(self):
        self.access = Access()
        self.db = Db()
        self.entity = Entity()
        self.execute = Execute()