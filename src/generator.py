from src.Instructions import I, Types

#macros
get_id = lambda dict, value : list(dict.keys()).index(value)
goto_start = lambda : "+[-<+]-"
goto_anchor = lambda value : f"{goto_start()} {'+'*value}[{'-'*value}>{'+'*value}]{'-'*value}"

class Generator:
    def __init__(self, debug):
        self.debug = debug
        self.instructions = ""
        self.integers_dict = {}
        self.strings_dict = {}
    
    def generate(self, instructions):
        self.instructions = instructions
    
    def add_instructions(self, instructions):
        self.instructions += instructions