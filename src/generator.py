from src.Instructions import I, Types
import datetime

#config
NUMBER_OF_RAMS = 5

#macros
goto_start = lambda : "+[-<+]-"

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
            if instruction[0] == I.PUSHINT:
                self.stack.append(instruction[1])
            if instruction[0] == I.PUSHWORD:
                self.stack.append(instruction[1])
            if instruction[0] == I.SET:
                name  = self.stack.pop()
                value = self.stack.pop()
                self.integers_dict[name] = value
                
        for instruction in instructions:
            if instruction[0] == I.SET:
                pass
        
        if self.debug : print(f"[DEBUG GENERATOR] instructions : {''.join([x for x in self.instructions if x in ['+','-','<','>','.',',','[',']']])}")
    
    def add_instructions(self, instructions):
        self.instructions += instructions