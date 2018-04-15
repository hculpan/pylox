from enum import Enum


class DataType(Enum):
    UNKNOWN = 1
    INTEGER = 2
    DOUBLE = 3
    STRING = 4
    BOOLEAN = 5
    NIL = 6
    FUNCTION = 7


class Data:
    def __init__(self, value, type):
        self.value = value
        self.type = type


