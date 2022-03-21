from src.Instructions import I, Types
import datetime

#config
NUMBER_OF_RAMS = 5

#macros
get_id = lambda dict, value : list(dict.keys()).index(value)
goto_start = lambda : "+[-<+]-"
goto_anchor = lambda value : f"{goto_start()} {'+'*value}[{'-'*value}>{'+'*value}]{'-'*value}"
goto_variables = lambda : f"{goto_anchor(2)}"
goto_strings = lambda : f"{goto_anchor(3)}"
goto_always_0 = lambda : f"{goto_start()} >"
# reset_rams = lambda : f"{goto_start()} > {'>[-]'*NUMBER_OF_RAMS}" # A TESTER

class Generator:
    def __init__(self, debug):
        self.debug = debug
        self.instructions = ""
        self.integers_dict = {}
        self.strings_dict = {}
    
    def generate(self, instructions):  # sourcery skip: raise-specific-error
        self.add_instructions("# code par Loris_redstone\n")
        self.add_instructions("# version 2\n")
        self.add_instructions(f"# date : {str(datetime.datetime.now()).replace('-', ' ').replace('.', ' ')}\n")
        self.add_instructions("# initialize\n")
        self.add_instructions("# main anchor :\n")
        self.add_instructions("- \n")
        self.add_instructions("# variables\n")
        self.add_instructions(f"{'>'*(NUMBER_OF_RAMS+1)} -- {goto_start()}\n")

        for instruction in instructions:
            if instruction[0] == I.DECLARE_INT:
                self.integers_dict[instruction[1]] = 0
            if instruction[0] == I.DECLARE_STR:
                self.strings_dict[instruction[1]] = "N"*instruction[2]
        self.add_instructions("# nombre de variables\n")
        self.add_instructions(f"{goto_variables()} > {'+'*len(self.integers_dict)} #{len(self.integers_dict)}\n")
        for _ in range(len(self.integers_dict)):
            self.add_instructions("> ")
        self.add_instructions(f"{goto_start()} # set toutes les variables a 0\n")
        self.add_instructions("# strings\n")
        self.add_instructions(f"{goto_variables()} {'>'*(len(self.integers_dict)+2)} --- {goto_start()}\n")
        self.add_instructions("# nombre de strings\n")
        self.add_instructions(f"{goto_strings()} > {'+'*len(self.strings_dict)} {goto_start()} #{len(self.strings_dict)}\n")
        self.add_instructions("# init des strings\n")
        self.add_instructions(f"{goto_strings()} >")
        for key in self.strings_dict:
            value = self.strings_dict[key]
            self.add_instructions(f"> {'+'*len(value)} {'>'*(len(value))} # init d'un string de longueur {len(value)}\n")
        self.add_instructions(f"{goto_start()}\n")

        self.add_instructions("\nCODE : \n")
        for instruction in instructions:
            if instruction[0] == I.SET:
                name = instruction[1]
                if name in self.integers_dict:
                    value = int(instruction[2])
                    index = get_id(self.integers_dict, name)
                    self.add_instructions(f"{goto_variables()} {'>'*(index+2)} [-] {'+'*value} {goto_start()} # set {name} = {value}\n")
                if name in self.strings_dict:
                    value = instruction[2].replace("\\N", " ").replace("\\n", "\n")[1:-1]
                    index_in_dict = get_id(self.strings_dict, name)
                    part_list = list(self.strings_dict.values())[:index_in_dict]
                    index = sum(len(part) for part in part_list) + len(part_list) + 1
                    self.add_instructions(f"{goto_strings()} > {'>'*index} # va au debut de la chaine {name} pour son set\n")
                    for i in range(len(value)):
                        if value[i] in "azertyuiopqsdfghjklmwxcvbn1234567890/*AZERTYUIOPQSDFGHJKLMWXCVBN":
                            self.add_instructions(f"#character {value[i]} : > [-] {'+'*ord(value[i])}\n")
                        else:
                            self.add_instructions(f"#character (ILLEGAL TO PRINT) : > [-] {'+'*ord(value[i])}\n")
            elif instruction[0] == I.PRINTINTEGER:
                name = instruction[1]
                index = get_id(self.integers_dict, name)
                self.add_instructions(f"{goto_variables()} {'>'*(index+2)} . {goto_start()} # print {name}\n")
            elif instruction[0] == I.PRINTINT:
                name = instruction[1]
                index = get_id(self.integers_dict, name)
                NB = 48
                self.add_instructions(f"{goto_variables()} {'>'*(index+2)} {'+'*NB} . {'-'*NB} {goto_start()} # print la vraie valeur de {name}\n")
            elif instruction[0] == I.PRINTSTRING:
                name = instruction[1]
                index_in_dict = get_id(self.strings_dict, name)
                part_list = list(self.strings_dict.values())[:index_in_dict]
                index = sum(len(part) for part in part_list) + len(part_list) + 1
                self.add_instructions(f"{goto_strings()} > {'>'*index} {'> .'*len(self.strings_dict[name])} {goto_start()} # print {name}\n")
            elif instruction[0] == I.IF:
                name = instruction[1]
                index = get_id(self.integers_dict, name)
                self.add_instructions(f"{goto_variables()}{'>'*(index+2)}[-{goto_start()}>+>+{goto_variables()}{'>'*(index+2)}] #load the value of {name} in ALWAYS_0 and IFTEMP \n")
                self.add_instructions(f"{goto_start()}>[-{goto_variables()}{'>'*(index+2)}+{goto_start()}>] #push back {name} in it's place and void ALWAYS_0\n")
                self.add_instructions(f"{goto_start()}>> [[-]+<] #normalize IFTEMP")
                if_instructions = instruction[2]
                if_generateur = Generator(self.debug)
                if_generateur.integers_dict = self.integers_dict
                if_generateur.strings_dict = self.strings_dict
                if_generateur.generate(if_instructions)
                newline = "\n"
                self.add_instructions(f"\n{goto_start()}>> #start of the if \n[-{f'{newline}    '.join(if_generateur.instructions.split('CODE :')[1].split(newline))}{goto_start()}\n>]# end of the if\n")
            elif instruction[0] == I.LOOP:
                name = instruction[1]
                index = get_id(self.integers_dict, name)
                self.add_instructions(f"{goto_variables()}{'>'*(index+2)}[-{goto_start()}>+>+{goto_variables()}{'>'*(index+2)}] #load the value of {name} in ALWAYS_0 and IFTEMP \n")
                self.add_instructions(f"{goto_start()}>[-{goto_variables()}{'>'*(index+2)}+{goto_start()}>] #push back {name} in it's place and void ALWAYS_0\n")
                if_instructions = instruction[2]
                loop_generateur = Generator(self.debug)
                loop_generateur.integers_dict = self.integers_dict
                loop_generateur.strings_dict = self.strings_dict
                loop_generateur.generate(if_instructions)
                newline = "\n"
                self.add_instructions(f"\n{goto_start()}>> #start of the loop \n[-{f'{newline}    '.join(loop_generateur.instructions.split('CODE :')[1].split(newline))}{goto_start()}\n>>] #end of the loop \n")
            elif instruction[0] == I.LOAD:
                load_to = int(instruction[1][3:])
                what_to_load = instruction[2]
                index = get_id(self.integers_dict, what_to_load)
                if load_to > NUMBER_OF_RAMS-2 :
                    raise Exception(f"Can't load into {load_to} because the maximum number of rams got reached")
                self.add_instructions(f"{goto_variables()}{'>'*(index+2)}[-{goto_start()}>+{'>'*(load_to+2)}+{goto_variables()}{'>'*(index+2)}] #load the value of {what_to_load} in ALWAYS_0 and ram{load_to} \n")
                self.add_instructions(f"{goto_start()}>[-{goto_variables()}{'>'*(index+2)}+{goto_start()}>] #push back {what_to_load} in it's place and void ALWAYS_0\n")
            elif instruction[0] == I.EQUAL: # might be a bug cause of the ram1+2
                ram1 = int(instruction[1][3:])
                ram2 = int(instruction[2][3:])
                diff = max((ram2 - ram1), (ram1 - ram2))
                self.add_instructions(f" {goto_start()} {'>'*(ram1+2)} {'>'*diff}[-{'<'*diff}-{'>'*diff}]+{'<'*diff}[{'>'*diff}-{'<'*diff}[-]]{'>'*diff}[-{'<'*diff}+{'>'*diff}] #computes the = of ram{ram1} and ram{ram2} \n")
            elif instruction[0] == I.STORE:
                where = instruction[1]
                what = int(instruction[2][3:])
                index = get_id(self.integers_dict, where)
                self.add_instructions(f"{goto_variables()}{'>'*(index+2)}[-] {goto_start()}{'>'*(what+3)} [- {goto_variables()}{'>'*(index+2)}+{goto_start()}{'>'*(what+3)}] #store the value of ram{what} in {where} \n")
            elif instruction[0] == I.INPUT:
                name = instruction[1]
                index = get_id(self.integers_dict, name)
                self.add_instructions(f"{goto_variables()}{'>'*(index+2)}, {goto_start()}")

        if self.debug : print("[DEBUG GENERATOR] integers_dict :", self.integers_dict)
        if self.debug : print("[DEBUG GENERATOR] strings_dict :", self.strings_dict)
        if self.debug : print(f"[DEBUG GENERATOR] instructions : {''.join([x for x in self.instructions if x in ['+','-','<','>','.',',','[',']']])}")
    
    def add_instructions(self, instructions):
        self.instructions += instructions