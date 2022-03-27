from enum import IntEnum, auto

class I(IntEnum):
    DECLARE_INT = auto()
    DECLARE_STR = auto()
    
    RAWPRINTSTRING = auto()
    PRINTSTRING = auto()
    PRINTINT = auto()
    PRINTINTEGER = auto()
    
    SET = auto()
    
    IF = auto()
    
class Types(IntEnum):
    INT = auto()
    STR = auto()