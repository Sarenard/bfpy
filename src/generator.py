from re import T
from src.Instructions import I, Types
import datetime

#macros
get_id = lambda dict, value : list(dict.keys()).index(value)
goto_start = lambda : "+[-<+]-"
goto_anchor = lambda value : f"{goto_start()} {'+'*value}[{'-'*value}>{'+'*value}]{'-'*value}"
goto_pile = lambda : goto_anchor(2)
goto_variables = lambda : goto_anchor(3)

TAILLE_PILE = 0
NOMBRE_DE_RAMS = 5
INDEX_DECALE = NOMBRE_DE_RAMS + TAILLE_PILE

class Generator:
    def __init__(self, debug):
        self.debug = debug
        self.instructions = ""
        self.variables = {}
        self.variables_indexes = {}
    
    def generate(self, instructions):
        self.add_instructions("# code par Loris_redstone\n")
        self.add_instructions("# version 3\n")
        self.add_instructions(f"# date : {str(datetime.datetime.now()).replace('-', ' ').replace('.', ' ')}\n")
        self.add_instructions("# initialize\n")
        self.add_instructions("# main anchor :\n")
        self.add_instructions("- \n")
        for instruction in instructions:
            match instruction:
                case I.DECLARE_INT, name, size:
                    value = 0
                    if size == 8:
                        self.variables_indexes[name] = len(self.variables)
                        self.variables[len(self.variables)] = {"type" : Types.INT, "name" : name, "value" : value, "size" : size, "linked" : 0, "position" : len(self.variables)}
                    else:
                        self.variables_indexes[name] = len(self.variables)
                        for i in range(int(size/8)):
                            self.variables[len(self.variables)] = {"type" : Types.INT, "name" : name, "value" : value, "size" : size, "linked" : (len(self.variables)+1 if int(size/8) != i+1 else 0), "position" : len(self.variables)}
                case I.DECLARE_STR, name, longueur:
                    start_index = len(self.variables)
                    for i in range(int(longueur)):
                        self.variables[len(self.variables)] = {"type" : Types.STR, "name" : name, "value" : "", "linked" : (len(self.variables)+1 if i != int(longueur)-1 else 0), "position" : len(self.variables)}
                    self.variables_indexes[name] = start_index
                case I.DECLARE_LIST, name, longueur:
                    raise NotImplementedError("Les listes sont pas implémentées, faut le faire sous la forme [*(value, anchor=249+)]")
                    start_index = len(self.variables)
                    self.variables[len(self.variables)] = {"type" : Types.LIST_CURRENT_INDEX, "name" : name, "value" : 0, "linked" : len(self.variables)+1, "position" : len(self.variables)}
                    for i in range(int(longueur)):
                        self.variables[len(self.variables)] = {"type" : Types.LIST, "name" : name, "value" : 0, "linked" : (len(self.variables)+1 if i != int(longueur)-1 else 0), "position" : len(self.variables)}
                    self.variables_indexes[name] = start_index
        if TAILLE_PILE != 0:
            self.add_instructions("#pile\n")
            self.add_instructions(f"{goto_start()}{'>'*(NOMBRE_DE_RAMS+1)} -- {'>'*len(self.variables)} ({len(self.variables)})\n")
            self.add_instructions("#nombre de variables\n")
            self.add_instructions(f"{goto_start()}> {'>'*(NOMBRE_DE_RAMS+1+TAILLE_PILE+1+1)} --- {'>'*len(self.variables)} ({len(self.variables)})\n")
        else:
            self.add_instructions("#nombre de variables\n")
            self.add_instructions(f"{goto_start()}> {'>'*(NOMBRE_DE_RAMS+1)} --- {'>'*len(self.variables)} ({len(self.variables)})\n")
        self.add_instructions("\n")
        self.add_instructions(f"CODE :\n")
        for instruction in instructions:
            match instruction:
                case I.SET, name, value:
                    start_index = self.variables_indexes[name]
                    data = self.variables[start_index]
                    if data["type"] == Types.INT:
                        if data["size"] == 8:
                            self.variables[start_index]["value"] = int(value)
                            self.add_instructions(f"{goto_variables()} {'>'*(start_index+1)} [-] {'+'*int(value)} # set la variable int ({name}) a {int(value)} \n")
                        else:
                            raise Exception("TODO : SET INT SIZE > 8")
                    if data["type"] == Types.STR:
                        toshow = value.replace('\n', '\\n')
                        self.add_instructions(f"# set la variable str ({name}) a \"{toshow.replace(',', ' ').replace('+', ' ').replace('-', ' ').replace('.', ' ').replace('[', ' ').replace(']', ' ').replace('>', ' ').replace('<', ' ')}\"\n")
                        for i in range(len(value)):
                            data["value"] = value[i]
                            index = data["position"]
                            nb = ord(value[i])
                            if value[i] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789?/;:":
                                self.add_instructions(f"{value[i]} : {goto_variables()} {'>'*(index+1)} [-] {'+'*int(nb)}\n")
                            else:
                                self.add_instructions(f"ILLEGAL TO PRINT : {goto_variables()} {'>'*(index+1)} [-] {'+'*int(nb)}\n")
                            data = self.variables[data["linked"]]
                case I.PRINTINTEGER, name:
                    start_index = self.variables_indexes[name]
                    data = self.variables[start_index]
                    if data["size"] == 8:
                        self.add_instructions(f"{goto_variables()} {'>'*(start_index+1)} .# print la variable int ({name}) \n")
                    else:
                        raise Exception("TODO : PRINTINTEGER INT SIZE > 8")
                case I.PRINTINT, name:
                    start_index = self.variables_indexes[name]
                    data = self.variables[start_index]
                    if data["size"] == 8:
                        self.add_instructions(f"{goto_variables()} {'>'*(start_index+1)} {'+'*48} . {'-'*48} # print la variable int ({name}) \n")
                    else:
                        raise Exception("TODO : PRINTINT INT SIZE > 8")
                case I.PRINTSTRING, name:
                    char = 0
                    start_index = self.variables_indexes[name]
                    data = self.variables[start_index]
                    self.add_instructions("# print la variable str ({name}) \n")
                    self.add_instructions(f"{goto_variables()} {'>'*(start_index+1)} .  # print la variable string ({name} | char={char} | value={data['value']}) \n")
                    while not data["linked"] == 0:
                        char += 1
                        self.add_instructions(f"{goto_variables()} {'>'*(data['linked']+1)} . # print la variable string ({name} | char={char} | value={data['value']}) \n")
                        data = self.variables[data["linked"]]
                case I.IF, name, if_instructions:
                    index = self.variables_indexes[name]
                    self.add_instructions(f"{goto_variables()}{'>'*(index+1)}[-{goto_start()}>+>+{goto_variables()}{'>'*(index+1)}] #load the value of {name} in ALWAYS_0 and IFTEMP \n")
                    self.add_instructions(f"{goto_start()}>[-{goto_variables()}{'>'*(index+1)}+{goto_start()}>] #push back {name} in it's place and void ALWAYS_0\n")
                    if_generateur = Generator(self.debug)
                    if_generateur.variables = self.variables
                    if_generateur.variables_indexes = self.variables_indexes
                    if_generateur.generate(if_instructions)
                    newline = "\n"
                    self.add_instructions(f"{goto_start()}>> #start of the if \n[[-]{f'{newline}    '.join(if_generateur.instructions.split('CODE :')[1].split(newline))}{goto_start()}\n>]# end of the if\n")
                case I.RAWPRINTSTRING, value:
                    # TODO : OPTIMISE AND DONT REDO ord(char) EACH TIME
                    to_show = ''.join([(x if x in 'abcdefghijklmnopqrstuvwxyz123456798ABCDEFGHIJKLMNOPQRSTUVWXYZ/*!:;§/?' else '|') for x in value])
                    self.add_instructions(f"PRINT 1 TIME STRING \"{to_show}\"\n")
                    to_print = "".join([f"{'+'*ord(char)}.[-]" for char in value])
                    self.add_instructions(f"{goto_start()} > {to_print}\n")
                case I.LOAD, load_to, what_to_load:
                    load_to = int(load_to[3:])
                    index = self.variables_indexes[what_to_load]
                    data = self.variables[index]
                    if data["size"] == 8:
                        if load_to > NOMBRE_DE_RAMS-2 :
                            raise Exception(f"Can't load into {load_to} because the maximum number of rams got reached")
                        self.add_instructions(f"{goto_variables()}{'>'*(index+1)}[-{goto_start()}>+{'>'*(load_to+2)}+{goto_variables()}{'>'*(index+1)}] #load the value of {what_to_load} in ALWAYS_0 and ram{load_to} \n")
                        self.add_instructions(f"{goto_start()}>[-{goto_variables()}{'>'*(index+1)}+{goto_start()}>] #push back {what_to_load} in it's place and void ALWAYS_0\n")
                    else:
                        raise Exception("TODO : LOAD INT SIZE > 8")
                case I.EQUAL, ram1, ram2:
                    ram1 = int(ram1[3:])
                    ram2 = int(ram2[3:])
                    diff = max((ram2 - ram1), (ram1 - ram2))
                    self.add_instructions(f"{goto_start()} {'>'*(ram1+3)} {'>'*diff}[-{'<'*diff}-{'>'*diff}]+{'<'*diff}[{'>'*diff}-{'<'*diff}[-]]{'>'*diff}[-{'<'*diff}+{'>'*diff}] #computes the = of ram{ram1} and ram{ram2} \n")
                case I.STORE, where, what:
                    what = int(what[3:])
                    index = self.variables_indexes[where]
                    data = self.variables[index]
                    if data["size"] == 8:
                        self.add_instructions(f"{goto_variables()}{'>'*(index+1)}[-] {goto_start()}{'>'*(what+3)} [- {goto_variables()}{'>'*(index+1)}+{goto_start()}{'>'*(what+3)}] #store the value of ram{what} in {where} \n")
                    else:
                        raise Exception("TODO : STORE INT SIZE > 8")
                case I.INPUT, name:
                    index = self.variables_indexes[name]
                    data = self.variables[index]
                    if data["size"] == 8:
                        self.add_instructions(f"{goto_variables()}{'>'*(index+1)}, #input in {name} \n")
                    else:
                        raise Exception("TODO : INPUT INT SIZE > 8")
                case I.CADD, name, number:
                    number = int(number)
                    index = self.variables_indexes[name]
                    data = self.variables[index]
                    if data["size"] == 8:
                        self.add_instructions(f"{goto_variables()}{'>'*(index+1)} {'+'*number if number > 0 else '-'*(-number)} {f'add {number}' if number > 0 else f'remove {-number}'} to {name} \n")
                    else:
                        raise Exception("TODO : CADD INT SIZE > 8")
                case I.ADD, var1, var2, to_store:
                    load_to, what_to_load = "ram0", var1
                    load_to = int(load_to[3:])
                    index = self.variables_indexes[what_to_load]
                    data1, data2, data3 = self.variables[index], self.variables[self.variables_indexes[var2]], self.variables[self.variables_indexes[to_store]]
                    if data1["size"] == data2["size"] == data3["size"] == 8:
                        if load_to > NOMBRE_DE_RAMS-2 :
                            raise Exception(f"Can't load into {load_to} because the maximum number of rams got reached")
                        self.add_instructions(f"{goto_variables()}{'>'*(index+1)}[-{goto_start()}>+{'>'*(load_to+2)}+{goto_variables()}{'>'*(index+1)}] #load the value of {what_to_load} in ALWAYS_0 and ram{load_to} \n")
                        self.add_instructions(f"{goto_start()}>[-{goto_variables()}{'>'*(index+1)}+{goto_start()}>] #push back {what_to_load} in it's place and void ALWAYS_0\n")
                        load_to, what_to_load = "ram1", var2
                        load_to = int(load_to[3:])
                        index = self.variables_indexes[what_to_load]
                        if load_to > NOMBRE_DE_RAMS-2 :
                            raise Exception(f"Can't load into {load_to} because the maximum number of rams got reached")
                        self.add_instructions(f"{goto_variables()}{'>'*(index+1)}[-{goto_start()}>+{'>'*(load_to+2)}+{goto_variables()}{'>'*(index+1)}] #load the value of {what_to_load} in ALWAYS_0 and ram{load_to} \n")
                        self.add_instructions(f"{goto_start()}>[-{goto_variables()}{'>'*(index+1)}+{goto_start()}>] #push back {what_to_load} in it's place and void ALWAYS_0\n")
                        self.add_instructions(f"{goto_start()}>>>> [-<+>]")
                        what, where = "ram0", to_store
                        what = int(what[3:])
                        index = self.variables_indexes[where]
                        self.add_instructions(f"{goto_variables()}{'>'*(index+1)}[-] {goto_start()}{'>'*(what+3)} [- {goto_variables()}{'>'*(index+1)}+{goto_start()}{'>'*(what+3)}] #store the value of ram{what} in {where} \n")
                    else:
                        raise Exception("TODO : ADD INT SIZE > 8")
                case I.WHILE, variable, while_instructions:
                    index = self.variables_indexes[variable]
                    data = self.variables[index]
                    if data["size"] == 8:
                        self.add_instructions(f"{goto_variables()}{'>'*(index+1)}[-{goto_start()}>+>+{goto_variables()}{'>'*(index+1)}] #load the value of {variable} in ALWAYS_0 and IFTEMP \n")
                        self.add_instructions(f"{goto_start()}>[-{goto_variables()}{'>'*(index+1)}+{goto_start()}>] #push back {variable} in it's place and void ALWAYS_0\n")
                        while_generateur = Generator(self.debug)
                        while_generateur.variables = self.variables
                        while_generateur.variables_indexes = self.variables_indexes
                        while_generateur.generate(while_instructions)
                        newline = "\n"
                        self.add_instructions(f"{goto_start()}>> [[-] #start of the while {f'{newline}    '.join(while_generateur.instructions.split('CODE :')[1].split(newline))}")
                        self.add_instructions(f"{goto_variables()}{'>'*(index+1)}[-{goto_start()}>+>+{goto_variables()}{'>'*(index+1)}]{goto_start()}>[-{goto_variables()}{'>'*(index+1)}+{goto_start()}>] #reload la variable pour le while \n>]# end of the while\n")
                    else:
                        raise Exception("TODO : WHILE INT SIZE > 8")
                case I.APPEND, name_list, name_value:
                    if self.variables[self.variables_indexes[name_value]]["size"] == 8:
                        
                        longueur_max = 250
                        load_to, what_to_load = int("ram2"[3:]), name_value
                        index = self.variables_indexes[what_to_load]
                        if load_to > NOMBRE_DE_RAMS-2 :
                            raise Exception(f"Can't load into {load_to} because the maximum number of rams got reached")
                        self.add_instructions(f"{goto_variables()}{'>'*(index+1)}[-{goto_start()}>+{'>'*(load_to+2)}+{goto_variables()}{'>'*(index+1)}]{goto_start()}>[-{goto_variables()}{'>'*(index+1)}+{goto_start()}>] # loads the length of the list in {load_to}\n")
                        self.add_instructions(f"{goto_variables()}{'>'*(index+1)}")
                        
                        load_to, what_to_load = int("ram1"[3:]), name_list
                        index = self.variables_indexes[what_to_load]
                        if load_to > NOMBRE_DE_RAMS-2 :
                            raise Exception(f"Can't load into {load_to} because the maximum number of rams got reached")
                        self.add_instructions(f"{goto_variables()}{'>'*(index+1)}[-{goto_start()}>+{'>'*(load_to+2)}+{goto_variables()}{'>'*(index+1)}]{goto_start()}>[-{goto_variables()}{'>'*(index+1)}+{goto_start()}>] # loads the length of the list in {load_to}\n")
                        self.add_instructions(f"{goto_variables()}{'>'*(index+1)}")
                        self.add_instructions(f">{'[-'*longueur_max}{'>]'*longueur_max}\n")
                        what, where = int("ram2"[3:]), self.variables_indexes[name_list]
                        index = self.variables_indexes[where]
                        data = self.variables[index]
                        self.add_instructions(f"{goto_variables()}{'>'*(index+1)}[-] {goto_start()}{'>'*(what+3)} [- {goto_variables()}{'>'*(index+1)}+{goto_start()}{'>'*(what+3)}] #store the value of ram{what} in {where} \n")
                        
                    else:
                        raise Exception("TODO : APPEND INT SIZE > 8")
    
    def add_instructions(self, instructions):
        self.instructions += instructions