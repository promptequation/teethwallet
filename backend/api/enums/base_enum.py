from enum import Enum


class BaseEnum(Enum):
    @property
    def value(self):
        return self._value_

    @property
    def name(self):
        return self._name_.replace('_', ' ').title()

    @classmethod
    def get_name_from_value(cls, value):
        if value:
            name = None
            for _i in cls:
                if _i.value == value:
                    name = _i.name
            return name
