from enum import Enum, IntEnum, auto

class I(IntEnum):
    PUSHINT = auto()
    PUSHWORD = auto()
    SET = auto()
    
class Types(IntEnum):
    INT = auto()
    STR = auto()