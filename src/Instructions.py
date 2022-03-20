from enum import Enum, IntEnum, auto

class I(IntEnum):
    PUSHINT = auto()
    PUSHSTR = auto()
    SET = auto()
    
class Types(IntEnum):
    INT = auto()
    STR = auto()