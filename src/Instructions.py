from enum import Enum, IntEnum, auto

class I1(IntEnum):
    PUSHINT = auto()
    PUSHSTR = auto()
    SET = auto()
    
class I2(IntEnum):
    pass
    
class Types(IntEnum):
    INT = auto()
    STR = auto()