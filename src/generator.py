from re import T
from tracemalloc import start
from src.Instructions import I, Types
import datetime

#macros
get_id = lambda dict, value : list(dict.keys()).index(value)
goto_start = lambda : "+[-<+]-"
goto_anchor = lambda value : f"{goto_start()}{'+'*value}[{'-'*value}>{'+'*value}]{'-'*value}"
goto_pile = lambda : goto_anchor(2)
goto_variables = lambda : goto_anchor(3)
to_print = lambda value :  f"[-]{'+'*ord(value[0])}."+"".join([f"{-nb*'+' if nb < 0 else nb*'-'}." for nb in [ord(value[x-1])-ord(value[x]) for x in range(1, len(value))]])+"[-]"

NOMBRE_DE_RAMS = 10
assert NOMBRE_DE_RAMS >= 10, "Nombre de RAMs insuffisant, merci de mettre 10 minimum"
assert NOMBRE_DE_RAMS == 10, "Penser a changer le nombre dans l'interpretuer"
INDEX_DECALE = NOMBRE_DE_RAMS

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
                    # TODO : NULL TERMINATED STRING + LENGTH TO SUPPORT EASELY ADDING THEM
                    start_index = len(self.variables)
                    for i in range(int(longueur)):
                        self.variables[len(self.variables)] = {"type" : Types.STR, "name" : name, "value" : "", "linked" : (len(self.variables)+1 if i != int(longueur)-1 else 0), "position" : len(self.variables)}
                    self.variables_indexes[name] = start_index
                case I.DECLARE_LIST, name, longueur:
                    # TODO : CHANGE THE 2N COMPLEXITY TO A N+1 COMPLEXITY
                    # TODO : make lists with stacks
                    start_index = len(self.variables)
                    self.variables[len(self.variables)] = {"type" : Types.INT, "name" : name, "value" : value, "size" : 8, "linked" : len(self.variables)+1, "position" : len(self.variables)} #TODO : ADAPT THE SIZE OF THE LENGTH OF THE LIST
                    for i in range(int(longueur)):
                        self.variables[len(self.variables)] = {"type" : Types.LIST_CURRENT_INDEX, "name" : name, "value" : 0, "linked" : len(self.variables)+1, "position" : len(self.variables), "len" : len(self.variables)-1}
                        self.variables[len(self.variables)] = {"type" : Types.LIST, "name" : name, "value" : 0, "linked" : (len(self.variables)+1 if i != int(longueur)-1 else 0), "position" : len(self.variables), "len" : len(self.variables)-1}
                    self.variables_indexes[name] = start_index
        self.add_instructions("#nombre de variables\n")
        self.add_instructions(f"{goto_start()}> {'>'*(NOMBRE_DE_RAMS+1)} --- {'>'*len(self.variables)} ({len(self.variables)})\n")
        if any(self.variables[i]["type"] == Types.LIST for i in self.variables):
            self.add_instructions("INIT DES LISTES : \n")
        for instruction in instructions:
            match instruction:
                case I.DECLARE_LIST, name, longueur:
                    index = self.variables_indexes[name]+1
                    data = self.variables[index]
                    self.add_instructions(f"{goto_variables()}{'>'*(index+1)}------\n")
        self.add_instructions("\n")
        self.add_instructions(f"CODE :\n")
        for instruction in instructions:
            match instruction:
                case I.SET, name, value:
                    start_index = self.variables_indexes[name]
                    data = self.variables[start_index]
                    if data["type"] == Types.INT:
                        value = int(value)
                        self.variables[start_index]["value"] = value
                        valeurs = [eval(f"{value}{'//250'*r}%250") for r in range(0, int(data["size"]/8))]
                        self.add_instructions(f"{goto_variables()} {'>'*(start_index+1)} [-] {'>'.join(['+'*int(valeur) for valeur in valeurs])} # set la variable int ({name}) a {int(value)} \n")
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
                    index = self.variables_indexes[name]
                    data = self.variables[index]
                    while not data["linked"] == 0:
                        self.add_instructions(f"{goto_variables()}{'>'*(index+1)}.")
                        index, data = index+1, self.variables[data["linked"]]
                    self.add_instructions(f"{goto_variables()}{'>'*(index+1)}.# print la variable int ({name}) \n")
                case I.PRINTINT, name:
                    # todo : print the real value instead
                    print_case = lambda index : f"{goto_variables()}{'>'*(index+1)}[-{goto_start()}>+{goto_variables()}{'>'*(index+1)}] {goto_start()}>>>++++++++++<<[->+>-[>+>>]>[+[-<+>]>+>>]<<<<<<]>>[-]>>>++++++++++<[->-[>+>>]>[+[-<+>]>+>>]<<<<<]>[-]>>[>++++++[-<++++++++>]<.<<+>+>[-]]<[<[->-<]++++++[->++++++++<]>.[-]]<<++++++[-<++++++++>]<.[-]<<[-<+>]{goto_start()}>[-{goto_variables()}{'>'*(index+1)}+{goto_start()}>]"
                    index = self.variables_indexes[name]
                    data = self.variables[index]
                    truc = 0
                    while not data["linked"] == 0:
                        self.add_instructions(f"{print_case(index)}{to_print(f'*250^{truc} ')}")
                        index, truc, data = index+1, truc+1, self.variables[index+1]
                    data = self.variables[data["linked"]]
                    self.add_instructions(f"{print_case(index)}{to_print(f'*250^{truc}')} # print la variable int ({name}) \n")
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
                    data = self.variables[index]
                    if data["size"] == 8:
                        index = self.variables_indexes[name]
                        self.add_instructions(f"{goto_variables()}{'>'*(index+1)}[-{goto_start()}>+>+{goto_variables()}{'>'*(index+1)}] #load the value of {name} in ALWAYS_0 and IFTEMP \n")
                        self.add_instructions(f"{goto_start()}>[-{goto_variables()}{'>'*(index+1)}+{goto_start()}>] #push back {name} in it's place and void ALWAYS_0\n")
                        if_generateur = Generator(self.debug)
                        if_generateur.variables = self.variables
                        if_generateur.variables_indexes = self.variables_indexes
                        if_generateur.generate(if_instructions)
                        newline = "\n"
                        self.add_instructions(f"{goto_start()}>> #start of the if \n[[-]{f'{newline}    '.join(if_generateur.instructions.split('CODE :')[1].split(newline))}{goto_start()}\n>]# end of the if\n")
                    else:
                        raise Exception("TODO : IF INT SIZE > 8")
                case I.RAWPRINTSTRING, value:
                    to_show = ''.join([(x if x in 'abcdefghijklmnopqrstuvwxyz123456798ABCDEFGHIJKLMNOPQRSTUVWXYZ/*!:;§/?' else '|') for x in value])
                    self.add_instructions(f"PRINT 1 TIME STRING \"{to_show}\" : ")
                    self.add_instructions(f"{goto_start()} > {to_print(value)}\n")
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
                    self.add_instructions(f"{goto_variables()}{'>'*(index+1)},{'>[-]'*((data['size']-8)//8)} #input in {name}\n")
                case I.CADD, name, number:
                    number = int(number)
                    index = self.variables_indexes[name]
                    data = self.variables[index]
                    # TODO : generalise to every data size
                    if data["size"] == 8:
                        copy_to_ram0 = f"{goto_variables()}{'>'*(index+1)}[-{goto_start()}>+>>+{goto_variables()}{'>'*(index+1)}]"
                        add_one = f"{goto_start()}>>>+"
                        compare_to_250 = f"{goto_start()}>>>>------<[->-<]+>[<->[-]]"
                        compare_to_0 = f"{goto_start()}>>>>[-]<[->-<]+>[<->[-]]"
                        do_truc_250 = f"{goto_start()}>>+>[<->-<<[-]>>]<[-<+>]"
                        do_truc_0 = f"{goto_start()}>>+>[-<->{goto_variables()}{'>'*(index+1)}[-]------{goto_start()}>>>]"
                        remove_one = f"{goto_start()}>>[[-]{goto_variables()}{'>'*(index+1)}-{goto_start()}>>]"
                        put_back0 = f"{goto_start()}>[-{goto_variables()}{'>'*(index+1)}+{goto_start()}>]{remove_one}"
                        put_back = f"{goto_start()}>[-{goto_variables()}{'>'*(index+1)}+{goto_start()}>]"
                        new_to_add = f"{copy_to_ram0}{add_one}{compare_to_250}{do_truc_250}{put_back}"
                        new_to_remove = f"{copy_to_ram0}{compare_to_0}{do_truc_0}{put_back0}"
                        # TODO : prendre la boucle et faire des boucles multiples
                        to_add = f"{goto_start()}>>>>>>>{'+'*abs(number)}[-{(new_to_add if number > 0 else new_to_remove)}{goto_start()}>>>>>>>]"
                        self.add_instructions(f"{to_add} {f'add {number}' if number > 0 else f'remove {-number}'} to {name}(8) \n")
                    elif data["size"] == 16:
                        # TODO : faire ça dans une boucle   
                        # TODO : prendre la boucle et faire des boucles multiples
                        copy = lambda nb : f"{goto_variables()}{'>'*(index+nb+1)}[-{goto_start()}>+>>+{goto_variables()}{'>'*(index+nb+1)}]"
                        add_one = f"{goto_start()}>>>+"
                        compare_to_250 = f"{goto_start()}>>>>------<[->-<]+>[<->[-]]"
                        do_truc_250 = f"{goto_start()}>>+>[<->-<<[-]>>>>>>+<<<<<]"
                        check_250 = f"{goto_start()}>>[[-]<+>]"
                        put_back = lambda nb : f"{goto_start()}>[-{goto_variables()}{'>'*(index+nb+1)}+{goto_start()}>]"
                        add_250_0 = f"{copy(0)}{add_one}{compare_to_250}{do_truc_250}{check_250}{put_back(0)}"
                        add_250_1 = f"{goto_start()}>>>>>>>[[-]{copy(1)}{add_one}{compare_to_250}{do_truc_250}{check_250}{put_back(1)}]"
                        reset = f"{goto_start()}>>>>>>>[-]"
                        add = f"{add_250_0}{add_250_1}{reset}"
                        if_0 = f"{goto_start()}>>+>[[-]<-<->>]<[[-]{goto_start()}>>>>>+{goto_start()}>>]{put_back(0)}"
                        set_249 = f"{goto_start()}>>>>>[{goto_variables()}{'>'*(index+1)}[-]-------{goto_start()}>]"
                        remove_250 = f"{goto_start()}>>>>>[{copy(1)}{goto_start()}>>+>[[-]<-<-{put_back(1)}{goto_start()}>]"
                        check_0 = f"{goto_start()}>>[[-]{goto_variables()}{'>'*(index+2)}[-]-------{goto_start()}>>[-]]{goto_start()}>>>>>[-]]"
                        remove = f"{copy(0)}{if_0}{set_249}{remove_250}{check_0}"
                        self.add_instructions(f"{add*abs(number) if number > 0 else remove*abs(number)} {f'add {number}' if number > 0 else f'remove {-number}'} to {name}(16) \n")
                    else:
                        raise Exception("TODO : CADD INT SIZE > 16")
                case I.WHILE, variable, while_instructions:
                    index = self.variables_indexes[variable]
                    data = self.variables[index]
                    # raise Exception("TODO : WHILE INT SIZE > 8")
                    load = lambda x : f"{f'{goto_start()}>>>+' if x == 0 else ''}{goto_start()}>>[>[-]]{goto_start()}>>>[{goto_variables()}{'>'*(index+x+1)}[-{goto_start()}>+>+{goto_variables()}{'>'*(index+x+1)}]{goto_start()}>[-{goto_variables()}{'>'*(index+x+1)}+{goto_start()}>]]"
                    truc = 0
                    load_var = f"{goto_start()}>>[-]"
                    while not data["linked"] == 0:
                        self.add_instructions(f"{load(truc)}")
                        load_var += f"{load(truc)}"
                        data, truc = self.variables[data["linked"]], truc+1
                    self.add_instructions(f"{load(truc)}{goto_start()}>>>[-] #load de la valeur\n")
                    load_var += f"{load(truc)}{goto_start()}>>>[-]"
                    while_generateur = Generator(self.debug)
                    while_generateur.variables, while_generateur.variables_indexes = self.variables, self.variables_indexes
                    while_generateur.generate(while_instructions)
                    newline = "\n"
                    self.add_instructions(f"{goto_start()}>> [[-] #load variable and start of the while {f'{newline}    '.join(while_generateur.instructions.split('CODE :')[1].split(newline))}")
                    self.add_instructions(f"{load_var} #reload la variable pour le while \n{goto_start()}>>]# end of the while\n")
                case I.APPEND, name_list, name_value:
                    data = self.variables[self.variables_indexes[name_value]]
                    if data["size"] == 8:
                        value_index = self.variables_indexes[name_value]
                        list_index = self.variables_indexes[name_list]+1
                        goto_current = f"{goto_variables()}{'>'*(list_index+1)}++++++[------>++++++]------>"
                        goto_ram0 = f"{goto_start()}>>>"
                        goto_value = f"{goto_variables()}{'>'*(value_index+1)}"
                        load_value = f"{goto_value}[-{goto_start()}>+>>+{goto_value}] #load the value of {name_value} into ram\n"
                        store_value = f"{goto_start()}>[-{goto_value}+{goto_start()}>]{goto_current}[-]{goto_ram0}[-{goto_current}+{goto_ram0}] #store it in the right place\n"
                        move_cursor = f"{goto_current}<++++++>>------ #change the list current cursor\n"
                        add_to_len = f"{goto_variables()}{'>'*(self.variables_indexes[name_list]+1)}+ #add one to the len of the list\n"
                        append = f"{load_value}{store_value}{move_cursor}{add_to_len}"
                        self.add_instructions(append)
                    else:
                        raise Exception("TODO : APPEND INT SIZE > 8")
                case I.REMOVE, name_list:
                    list_index = self.variables_indexes[name_list]
                    self.add_instructions(f"{goto_variables()}{'>'*(list_index+1)}++++++[------>++++++]------<[-]>++++++<<------#remove the last element of {name_list}\n")
                    self.add_instructions(f"{goto_variables()}{'>'*(self.variables_indexes[name_list]+1)}- #remove one to the len of the list\n")
                case I.GETLEN, name_list, int_name:
                    data = self.variables[self.variables_indexes[int_name]]
                    if data["size"] == 8:
                        list_index = self.variables_indexes[name_list]
                        int_index = self.variables_indexes[int_name]
                        goto_len_list = f"{goto_variables()}{'>'*(list_index+1)}"
                        goto_int = f"{goto_variables()}{'>'*(int_index+1)}"
                        self.add_instructions(f"{goto_len_list}[-{goto_start()}>+>>+{goto_len_list}]{goto_start()}>[-{goto_len_list}+{goto_start()}>] #load the value into ram\n")
                        self.add_instructions(f"{goto_start()}>>>[-{goto_int}+{goto_start()}>>>] #put it in the int\n")
                    else:
                        raise Exception("TODO : GETLEN INT SIZE > 8")
                case I.TAKEPART, name_var, part, where_to_store:
                    if self.variables[self.variables_indexes[where_to_store]]["size"] == 8:
                        var_index = self.variables_indexes[name_var]
                        case_size = self.variables[var_index]["size"]//8-1
                        if part > case_size:
                            raise Exception(f"Can't take the part {part} of an int with size {case_size}")
                        to_store_index = self.variables_indexes[where_to_store]
                        goto_var = f"{goto_variables()}{'>'*(var_index+1+part)}"
                        goto_store = f"{goto_variables()}{'>'*(to_store_index+1)}"
                        self.add_instructions(f"{goto_store}[-]")
                        self.add_instructions(f"{goto_var}[-{goto_start()}>+>+{goto_var}]{goto_start()}>[-{goto_var}+{goto_start()}>]")
                        self.add_instructions(f"{goto_start()}>>[-{goto_store}+{goto_start()}>>] # store part {part} of {name_var} into {where_to_store}\n")
                    else:
                        raise Exception("Can't store a part of an int in a non 8 bit int !")
                case I.SETPART, name_var, part, where_to_store:
                    if self.variables[self.variables_indexes[where_to_store]]["size"] == 8:
                        var_index = self.variables_indexes[name_var]
                        to_store_index = self.variables_indexes[where_to_store]
                        goto_var = f"{goto_variables()}{'>'*(var_index+1+part)}"
                        goto_store = f"{goto_variables()}{'>'*(to_store_index+1)}"
                        self.add_instructions(f"{goto_var}[-]")
                        self.add_instructions(f"{goto_store}[-{goto_start()}>+>+{goto_store}]{goto_start()}>[-{goto_store}+{goto_start()}>]")
                        self.add_instructions(f"{goto_start()}>>[-{goto_var}+{goto_start()}>>] # store part {part} of {name_var} into {where_to_store}\n")
                    else:
                        raise Exception("Can't set from an non 8 bit int !")
    
    def add_instructions(self, instructions):
        self.instructions += instructions