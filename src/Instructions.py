from enum import IntEnum, auto

class I(IntEnum):
    DECLARE_INT = auto()
    DECLARE_STR = auto()
    DECLARE_LIST = auto()
    
    RAWPRINTSTRING = auto()
    PRINTSTRING = auto()
    PRINTINT = auto()
    PRINTINTEGER = auto()
    
    SET = auto()
    INPUT = auto()
    APPEND = auto()
    REMOVE = auto()
    
    IF = auto()
    WHILE = auto()
    
    EQUAL = auto()
    CADD = auto()
    ADD = auto()
    
    LOAD = auto()
    STORE = auto()
    
class Types(IntEnum):
    INT = auto()
    STR = auto()
    LIST = auto()
    LIST_CURRENT_INDEX = auto()