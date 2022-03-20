from src.Instructions import I, Types
import datetime

class Generator:
    def __init__(self, debug):
        self.debug = debug
        self.instructions = ""
    
    def generate(self, instructions):
        self.add_instructions("# code par Loris_redstone\n")
        self.add_instructions("# version 2\n")
        self.add_instructions(f"# date : {str(datetime.datetime.now()).replace('-', ' ').replace('.', ' ')}\n")
        self.add_instructions("# initialize\n")
        self.add_instructions("# main anchor :\n")
        self.add_instructions("- \n")
        self.add_instructions("\n")
        
        if self.debug : print("[DEBUG] instructions :", "".join([x for x in instructions if x in ["+","-","<",">",".",",","[","]"]]))
    
    def add_instructions(self, instructions):
        self.instructions += instructions