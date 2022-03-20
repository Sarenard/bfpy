from enum import IntEnum, auto

class I(IntEnum):
    DECLARE_INT = auto()
    DECLARE_STR = auto()
    PRINTINTEGER = auto()
    PRINTINT = auto() #print la vraie valeur
    PRINTSTRING = auto()
    
    SET = auto()
    
class Types(IntEnum):
    INT = auto()
    STR = auto()