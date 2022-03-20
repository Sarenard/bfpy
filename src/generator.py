from src.Instructions import I, Types
import datetime

#config
NUMBER_OF_RAMS = 5

#macros
get_id = lambda dict, value : list(dict.keys()).index(value)
goto_start = lambda : "+[-<+]-"
goto_anchor = lambda value : f"{goto_start()} {'+'*value}[{'-'*value}>{'+'*value}]{'-'*value}"
goto_variables = lambda : goto_anchor(2)

class Generator:
    def __init__(self, debug):
        self.debug = debug
        self.instructions = ""
        self.stack = []
        self.integers_dict = {}
    
    def generate(self, instructions):
        self.add_instructions("# code par Loris_redstone\n")
        self.add_instructions("# version 2\n")
        self.add_instructions(f"# date : {str(datetime.datetime.now()).replace('-', ' ').replace('.', ' ')}\n")
        self.add_instructions("# initialize\n")
        self.add_instructions("# main anchor :\n")
        self.add_instructions("- \n")
        self.add_instructions("# variables\n")
        self.add_instructions(f"{'>'*(NUMBER_OF_RAMS+1)} -- {goto_start()}\n")
        self.add_instructions("\n")
        
        for instruction in instructions:
            if instruction[0] == I.DECLARE_INT:
                self.integers_dict[instruction[1]] = 0
        self.add_instructions("# nombre de variables\n")
        self.add_instructions(f"{goto_variables()} > {'+'*len(self.integers_dict)} #{len(self.integers_dict)}\n")
        for _ in range(len(self.integers_dict)):
            self.add_instructions(">")
        self.add_instructions(f" {goto_start()} # set toutes les variables a 0\n")
        
        self.add_instructions("\nCODE : \n")
        for instruction in instructions:
            if instruction[0] == I.SET:
                name = instruction[1]
                if name in self.integers_dict:
                    value = int(instruction[2])
                    index = get_id(self.integers_dict, name)
                    self.add_instructions(f"{goto_variables()} {'>'*(index+1)} [-] {'+'*value} {goto_start()} # set {name} = {value}\n")
            if instruction[0] == I.PRINTINTEGER:
                name = instruction[1]
                index = get_id(self.integers_dict, name)
                self.add_instructions(f"{goto_variables()} {'>'*(index+1)} . {goto_start()} # print {name}\n")
            if instruction[0] == I.PRINTINT:
                name = instruction[1]
                index = get_id(self.integers_dict, name)
                self.add_instructions(f"{goto_variables()} {'>'*(index+1)} {'+'*48} . {'-'*48} {goto_start()} # print la vraie valeur de {name}\n")
                
        if self.debug : print("[DEBUG GENERATOR] integers_dict :", self.integers_dict)
        if self.debug : print(f"[DEBUG GENERATOR] instructions : {''.join([x for x in self.instructions if x in ['+','-','<','>','.',',','[',']']])}")
    
    def add_instructions(self, instructions):
        self.instructions += instructions