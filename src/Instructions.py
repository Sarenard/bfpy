from enum import IntEnum, auto

class I(IntEnum):
    DECLARE_INT = auto()
    DECLARE_STR = auto()
    
    RAWPRINTSTRING = auto()
    PRINTSTRING = auto()
    PRINTINT = auto()
    PRINTINTEGER = auto()
    
    SET = auto()
    INPUT = auto()
    
    IF = auto()
    
    EQUAL = auto()
    
    LOAD = auto()
    STORE = auto()
    
class Types(IntEnum):
    INT = auto()
    STR = auto()