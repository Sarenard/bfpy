
# config
MAX_MACROS = 100
INDEX_OF_VARS = 6

# macros
goto_start = lambda : "+[-<+]-"
goto_anchor = lambda id : f"{goto_start()}{'+'*id}[{'-'*id}>{'+'*id}]{'-'*id}>"
goto_variables = lambda : f"{goto_anchor(2)}"
goto_strings = lambda : f"{goto_anchor(3)}"
get_index = lambda dictionnaire, valeur : list(dictionnaire).index(valeur)
replace_new_lines = lambda texte : texte.replace('\n', '\\n')
goto_variable = lambda variables, variable : f"{goto_variables()} {'>'*(get_index(variables, variable)+1)}"
set_var = lambda value : f"[-]{'+'*value} {goto_start()}"
print_integer = lambda : f"{'+'*48}.{'-'*48}"

class Generateur:
    def __init__(self, code, debug):
        self.debug = debug
        if self.debug : print(f"[DEBUG] Code : {replace_new_lines(code)}")
        self.code = code.replace("\n", " ").split(" ")
        if self.debug : print(f"[DEBUG] Code listé : {self.code}")
        self.instructions = ""
        self.nb_variables_int = 0
        self.nb_variables_str = 0
        self.variables_int = {}
        self.variables_str = {}
        self.str_stack = []
        self.int_stack = []
        self.stack = []
        self.total_macros = 0
        self.liste_included = []
        self.longueur_strings = []
    def generate_instructions(self):
        self.code = self.parse_includes(self.code)
        self.code = self.parse_macros(self.code)
        self.add_instructions("#Génération du brainfuck \n")
        self.add_instructions("#Auteur : Lorisredstone \n\n")
        self.add_instructions("# Anchor principale \n")
        self.add_instructions("-\n")
        self.add_instructions("# Anchor des variables\n")
        self.add_instructions(f"{'>'*INDEX_OF_VARS}-- {goto_start()}\n\n")
        instructions_index = 0
        last = []
        while instructions_index < len(self.code):
            instruction = self.code[instructions_index]
            if instruction.isdecimal():
                last.append("int")
                self.int_stack.append(int(instruction))
            elif instruction == "set":
                last.pop()
                name = self.stack.pop()
                dernier = last.pop()
                if dernier == "int":
                    value = self.int_stack.pop()
                elif dernier == "str":
                    value = self.str_stack.pop()
                elif dernier == "stk":
                    value = self.stack.pop()
                if name not in self.variables_int and dernier == "int":
                    self.variables_int[name] = value
                    self.nb_variables_int += 1
                if name not in self.variables_str and dernier == "str":
                    self.variables_str[name] = value
                    self.nb_variables_str += 1
            elif instruction.startswith("\"") and instruction.endswith("\""):
                last.append("str")
                self.str_stack.append(instruction[1:-1])
            else:
                self.stack.append(instruction)
                last.append("stk")
            instructions_index += 1
            
        self.nb_strings = len(self.str_stack)
        if self.debug : print(f"[DEBUG] Nombre de variables : {self.nb_strings}")
        if self.debug : print(f"[DEBUG] Liste des variables : {self.str_stack}")
        self.str_stack = []
        self.stack = []
        self.variables_int2 = [variable[0] for variable in self.variables_int.items()]
        self.variables_str2 = [variable[0] for variable in self.variables_str.items()]
        
        self.add_instructions(f"{goto_variables()}{'>'*self.nb_variables_int}>---{goto_start()}\n")
        
        if self.debug : print(f"[DEBUG] Nombre de variables : {self.nb_variables_int}")
        if self.debug : print(f"[DEBUG] Liste des variables : {self.variables_int2}")
        self.add_instructions(f"{goto_variables()} # go au début et va sur la case des variables\n")
        self.add_instructions(f"{set_var(self.nb_variables_int)} # nombre de variables ({self.nb_variables_int})\n")
        self.add_instructions(f"{goto_strings()} # go au début et va sur la case des strings\n")
        self.add_instructions(f"{set_var(self.nb_variables_str)} # nombre de strings ({self.nb_variables_str})\n")
        self.add_instructions("\n# CODE :\n")
        instructions_index = 0
        while instructions_index < len(self.code):
            instruction = self.code[instructions_index]
            if instruction.isdecimal():
                self.stack.append(int(instruction))
            elif instruction == "set":
                name = self.stack.pop()
                value = self.stack.pop()
                if isinstance(value, int):
                    self.add_instructions(f"{goto_variable(self.variables_int2, name)} {set_var(value)} # set la variable {name} = {value}\n")
                if isinstance(value, str):
                    self.longueur_strings.append(len(value))
                    value = value.replace('\\N', " ")
                    value = value.replace('\\n', "\n")
                    self.add_instructions(f"# stocke {value}")
                    self.add_instructions(f"{goto_strings()}{'>'*(len(self.longueur_strings[0:-1])+1+sum(self.longueur_strings[0:-1]))} # va au bon endroit\n") 
                    self.add_instructions(f"{'+'*len(value)}> #push la len\n")
                    newline = "\n"
                    for i in range(len(value)):
                        self.add_instructions(f"{value[i]} : {'+'*ord(value[i])}{'>' if not i == len(value)-1 else ''}{newline if not i == len(value)-1 else ''}")
                    self.add_instructions(f"{goto_start()} #retourne au début \n\n")
            elif instruction == "printstr":
                name = self.stack.pop()
                nb = len(self.variables_str[name].replace("\\n", "\n").replace("\\N", " "))
                index = get_index(self.variables_str, name)
                self.add_instructions(f"{goto_strings()} {'>'*(sum(self.longueur_strings[0:index])+index+2)}")
                for i in range(nb):
                    self.add_instructions(f".{'>' if not i == nb-1 else ''}")
                self.add_instructions(f" #affiche {self.variables_str[name]}")
            elif instruction == "printinteger":
                name = self.stack.pop()
                self.add_instructions(f"{goto_variable(self.variables_int2, name)} {print_integer()} # print la variable {name} en int\n")
            elif instruction == "printint":
                name = self.stack.pop()
                self.add_instructions(f"{goto_variable(self.variables_int2, name)} . # print la variable {name}\n")
            elif instruction == "input":
                name = self.stack.pop()
                self.add_instructions(f"{goto_variable(self.variables_int2, name)},{goto_start()} # input dans la variable {name}")
            elif instruction == "load":
                load_to = self.stack.pop()
                load_from = self.stack.pop()
                self.add_instructions(f"{goto_variable(self.variables_int2, load_from)}-[{goto_start()}{'>'*(int(load_to[3])+1)}+{goto_start()}>>>>+{goto_variable(self.variables_int2, load_from)}-]{goto_start()}{'>'*(int(load_to[3])+1)}+{goto_start()}>>>>+ #dupe and load {load_from} in {load_to} \n")
                self.add_instructions(f"{goto_start()} >>>>- [ {goto_variable(self.variables_int2, load_from)}+{goto_start()} >>>>-]{goto_variable(self.variables_int2, load_from)}+ # push back the original value \n")
            elif instruction == "=":
                from1 = self.stack.pop()
                id_from1 = int(from1[3])+1
                from2 = self.stack.pop()
                id_from2 = int(from2[3])+1
                self.add_instructions(f"{goto_start()} >> >>[-]>[-] <<<[>>>+<<<-]+ >[>>-<+<-] >[<+>-] >[<<<->>>[-]] << [-] < [-<+>] ")
            elif instruction == "+":
                from1 = self.stack.pop()
                id_from1 = int(from1[3])+1
                from2 = self.stack.pop()
                id_from2 = int(from2[3])+1
                self.add_instructions(f"{goto_start()}{'>'*id_from1}- [{goto_start()}>+{goto_start()}{'>'*id_from1}-]{goto_start()}>+ # load la value 1 dans l'adder\n")
                self.add_instructions(f"{goto_start()}{'>'*id_from2}- [{goto_start()}>+{goto_start()}{'>'*id_from2}-]{goto_start()}>+ # load la value 2 dans l'adder \n")
            elif instruction == "store_result":
                load_to = self.stack.pop()
                self.add_instructions(f"{goto_start()}>  [-[{goto_variable(self.variables_int2, load_to)}+{goto_start()}>-]{goto_variable(self.variables_int2, load_to)}+{goto_start()}>[-]] # store le résultat dans la variable {load_to}\n")
            elif instruction == "swap":
                nb = int(self.stack.pop())
                liste = [self.stack.pop() for _ in range(nb)]
                self.stack.append(liste[0])
                self.stack.extend(liste[x] for x in range(nb-1, 0, -1))
            elif instruction == "dup":
                item = self.stack.pop()
                self.stack.append(item)
                self.stack.append(item)
            elif instruction.startswith("\"") and instruction.endswith("\""):
                self.stack.append(instruction[1:-1])
            else:
                self.stack.append(instruction)
            instructions_index += 1

        
    def add_instructions(self, instructions):
        self.instructions += instructions
        
    def check_for_infinite_loop(self):
        if self.total_macros > MAX_MACROS:
            raise Exception("Too many nested macros")
    
    def parse_includes(self, instructions):
        if self.debug : print("[DEBUG] includes avant :", instructions, "liste modules inclus:", self.liste_included)
        liste_includes = []
        for i in range(max(len(instructions)-2, 1)):
            if instructions[i] == "#include":
                if instructions[i+1] not in self.liste_included:
                    self.liste_included.append(instructions[i+1])
                    liste_includes.append((instructions[i], instructions[i+1]))
                    instructions[i] = f'{instructions[i]} {instructions[i+1]}'
                    del instructions[i+1]
                else:
                    self.liste_included.append(instructions[i+1])
                    instructions[i] = f'{instructions[i]} {instructions[i+1]}'
                    del instructions[i+1]
                    del instructions[i]
        for include in liste_includes:
            content = open(include[1]).read().replace("\n", " ").split(" ")
            def replace(liste, element, truc):
                liste2 = []
                for x in liste:
                    if x == element:
                        liste2 += truc
                    else:
                        liste2.append(x)
                return liste2
            instructions = replace(instructions, f'{include[0]} {include[1]}', content)
        if self.debug : print("[DEBUG] includes apres :", instructions, "liste modules inclus:", self.liste_included)
        instructions = [x.replace("\n", " ") for x in instructions if x not in ["", " ", "\n"]]
        instructions2 = []
        for truc in instructions:
            if truc.startswith("\n"):
                instructions2.append(truc.split("\n")[1])
            elif truc.endswith("\n"):
                instructions2.append(truc.split("\n")[0])
            else:
                instructions2.append(truc)
        instructions = instructions2
        if sum(True for x in instructions if x == "#include") > 0:
            self.total_include += 1
            self.check_for_infinite_loop()
            instructions = self.parse_includes(instructions)
        return instructions
    def parse_macros(self, content, macros_total=[]):  # sourcery no-metrics skip: comprehension-to-generator, default-mutable-arg, hoist-statement-from-if, swap-nested-ifs
        if "iteration" not in globals() : globals()["iteration"]=1
        else: globals()["iteration"] += 1
        if self.debug : print(f"[DEBUG] macros avant (iteration {globals()['iteration']}) :", content)
        macros_total = macros_total
        macro_temp = []
        macro_en_cours = False
        content_remplacement = []
        end_compteur = 0
        for i in range(len(content)):
            if not macro_en_cours and content[i] != "macro" : content_remplacement.append(content[i])
            if content[i] == "macro":
                macro_en_cours = True
            if content[i] in ["if", "while"]:
                end_compteur += 1
            if content[i] == "end":
                if end_compteur == 0:
                    macro_en_cours = False
                    try:
                        macros_total.append((macro_temp[1], macro_temp[2:]))
                    except:
                        pass
                    macro_temp = []
                else:
                    end_compteur -= 1
            if macro_en_cours:
                macro_temp.append(content[i])
        content = content_remplacement
        if self.debug : print(f"[DEBUG] macros pendant (iteration {globals()['iteration']}) : macros:{macros_total}, content:{content}")
        content_remplacement = []
        for item in content:
            for macro in macros_total:
                if macro[0] == item:
                    content_remplacement += macro[1]
            if not sum(macro[0] == item for macro in macros_total):
                content_remplacement.append(item)
        content = content_remplacement
        if self.debug : print(f"[DEBUG] macros après (iteration {globals()['iteration']}) :", content)
        if sum([macro[0] == content[i] for macro in macros_total for i in range(len(content))]):
            self.total_macros += 1
            self.check_for_infinite_loop()
            content = self.parse_macros(content, macros_total)
        return content