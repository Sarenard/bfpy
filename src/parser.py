from src.Instructions import I1, I2, Types

# config
MAX_MACROS = 1000
MAX_INCLUDES = 1000

class Parser:
    def __init__(self, debug):
        self.debug = debug
        self.total_macros = 0
        self.total_includes = 0
        self.instructions = []
        self.liste_included = []
        self.stack = []
        
    def parse(self, instructions):
        self.instructions = instructions
        
        if self.debug : print(f"[DEBUG PARSER] instructions : {self.instructions}")