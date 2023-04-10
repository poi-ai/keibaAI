from base import Base
import datetime

class Horses(Base):
    def __init__(self):
        super().__init__()
        self.jbis_id = 0
        self.father_name = ''
        self.father_jbis_id = None
        self.mother_name = ''
        self.mother_jbis_id = None
        self.birth_day = None
        self.birth_place = ''
        self.breeder = ''
        self.hair_color = ''

    @property
    def jbis_id(self):
        return self._jbis_id

    @jbis_id.setter
    def jbis_id(self, value):
        if not isinstance(value, int):
            self.validate_error('jbis_id', 'jbis_idはint型である必要があります')
            return False
        self._jbis_id = value
        return True

    @property
    def father_name(self):
        return self._father_name

    @father_name.setter
    def father_name(self, value):
        self._father_name = value

    @property
    def father_jbis_id(self):
        return self._father_jbis_id

    @father_jbis_id.setter
    def father_jbis_id(self, value):
        if value is not None and not isinstance(value, int):
            self.validate_error('father_jbis_id', 'father_jbis_idはint型もしくはNoneである必要があります')
            return False
        self._father_jbis_id = value
        return True

    @property
    def mother_name(self):
        return self._mother_name

    @mother_name.setter
    def mother_name(self, value):
        self._mother_name = value

    @property
    def mother_jbis_id(self):
        return self._mother_jbis_id

    @mother_jbis_id.setter
    def mother_jbis_id(self, value):
        if value is not None and not isinstance(value, int):
            self.validate_error('mother_jbis_id', 'mother_jbis_idはint型もしくはNoneである必要があります')
            return False
        self._mother_jbis_id = value
        return True

    @property
    def birth_day(self):
        return self._birth_day

    @birth_day.setter
    def birth_day(self, value):
        if value is not None and not isinstance(value, datetime.date):
            self.validate_error('birth_day', 'birth_dayはdatetime.date型もしくはNoneである必要があります')
            return False
        self._birth_day = value
        return True

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, value):
        self._country = value

    @property
    def birth_place(self):
        return self._birth_place

    @birth_place.setter
    def birth_place(self, value):
        self._birth_place = value

    @property
    def breeder(self):
        return self._breeder

    @breeder.setter
    def breeder(self, value):
        self._breeder = value

    @property
    def hair_color(self):
        return self._hair_color

    @hair_color.setter
    def hair_color(self, value):
        self._hair_color = value