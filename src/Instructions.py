from enum import Enum, IntEnum, auto

class I(IntEnum):
    PUSHINT = auto()
    PUSHWORD = auto()
    DECLARE_INT = auto()
    PRINTINTEGER = auto()
    PRINTINT = auto()
    SET = auto()
    
class Types(IntEnum):
    INT = auto()
    STR = auto()