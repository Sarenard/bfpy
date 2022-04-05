from src.Instructions import I

# config
MAX_MACROS = 1000
MAX_INCLUDES = 1000

class Lexer:
    def __init__(self, debug):
        self.debug = debug
        self.total_macros = 0
        self.total_includes = 0
        self.instructions = []
        self.liste_included = []
        
    def parse(self, instructions):
        instructions = self.parse_includes(instructions)
        instructions = self.parse_macros(instructions)
        
        instruction_index = 0
        while instruction_index < len(instructions):
            instruction = instructions[instruction_index]
            if instruction == "#declare":
                if instructions[instruction_index + 1] in ["int", "8int"]:
                    name = instructions[instruction_index + 2]
                    self.instructions.append((I.DECLARE_INT, name, 8))
                    instruction_index += 2
                elif instruction[instruction_index + 1].split("int")[0] != "8":
                    name = instructions[instruction_index + 2]
                    size = instructions[instruction_index + 1].split("int")[0]
                    if not size % 8 == 0:
                        raise Exception("Size of int must be divisible by 8")
                    self.instructions.append((I.DECLARE_INT, name, int(size)))
                    instruction_index += 2
                if instructions[instruction_index + 1] == "str":
                    name = instructions[instruction_index + 2]
                    longueur = instructions[instruction_index + 3]
                    self.instructions.append((I.DECLARE_STR, name, longueur))
                    instruction_index += 3
            elif instruction == "printstring":
                name = instructions[instruction_index - 1]
                self.instructions.append((I.PRINTSTRING, name))
            elif instruction == "printint":
                name = instructions[instruction_index - 1]
                self.instructions.append((I.PRINTINT, name))
            elif instruction == "printinteger":
                name = instructions[instruction_index - 1]
                self.instructions.append((I.PRINTINTEGER, name))
            elif instruction == "rawprintstring":
                content = instructions[instruction_index - 1]
                self.instructions.append((I.RAWPRINTSTRING, content.replace("\\N", " ").replace("\\n", "\n").replace("\"", "")))
            elif instruction == "set":
                value = instructions[instruction_index - 2]
                name = instructions[instruction_index - 1]
                self.instructions.append((I.SET, name, value.replace("\\N", " ").replace("\\n", "\n").replace("\"", "")))
            elif instruction == "if":
                name = instructions[instruction_index-1]
                temp_instructions = ""
                end_counters = 0
                while True:
                    if instruction in ["if", "while", ]:
                        end_counters += 1
                    if instruction == "end":
                        end_counters -= 1
                        if end_counters == 0 :
                            break
                    temp_instructions += f'{instruction} '
                    instruction_index += 1
                    instruction = instructions[instruction_index]
                instruction_index += 1
                temp_instructions = " ".join(temp_instructions.split(" ")[1:])
                temp_instructions = temp_instructions.split(" ")
                if_lexer = Lexer(self.debug)
                if_lexer.parse(temp_instructions)
                self.instructions.append((I.IF, name, if_lexer.instructions, ))
            elif instruction == "load":
                load_to = instructions[instruction_index - 1]
                what_to_load = instructions[instruction_index - 2]
                self.instructions.append((I.LOAD, load_to, what_to_load))
            elif instruction == "=":
                ram2 = instructions[instruction_index - 1]
                ram1 = instructions[instruction_index - 2]
                self.instructions.append((I.EQUAL, ram1, ram2))
            elif instruction == "store":
                where = instructions[instruction_index - 1]
                what = instructions[instruction_index - 2]
                self.instructions.append((I.STORE, where, what))
            elif instruction == "input":
                what = instructions[instruction_index - 1]
                self.instructions.append((I.INPUT, what))
            elif instruction == "cadd":
                variable = instructions[instruction_index - 1]
                number = instructions[instruction_index - 2]
                self.instructions.append((I.CADD, variable, number))
            elif instruction == "add":
                var1 = instructions[instruction_index - 1]
                var2 = instructions[instruction_index - 2]
                to_store = instructions[instruction_index - 3]
                self.instructions.append((I.ADD, var1, var2, to_store))
            elif instruction == "while":
                name = instructions[instruction_index-1]
                temp_instructions = ""
                end_counters = 0
                while True:
                    if instruction in ["if", "while"]:
                        end_counters += 1
                    if instruction == "end":
                        end_counters -= 1
                        if end_counters == 0 :
                            break
                    temp_instructions += f'{instruction} '
                    instruction_index += 1
                    instruction = instructions[instruction_index]
                instruction_index += 1
                temp_instructions = " ".join(temp_instructions.split(" ")[1:])
                temp_instructions = temp_instructions.split(" ")
                if_lexer = Lexer(self.debug)
                if_lexer.parse(temp_instructions)
                self.instructions.append((I.WHILE, name, if_lexer.instructions, ))

            instruction_index += 1
            
        if self.debug : print("[DEBUG LEXER] instructions :", self.instructions)
        
    def check_for_infinite_loop(self):  # sourcery skip: raise-specific-error
        if self.total_macros > MAX_MACROS:
            raise Exception("Too many nested macros")
        if self.total_includes > MAX_INCLUDES:
            raise Exception("Too many nested includes")
    
    def parse_includes(self, instructions):
        if self.debug : print("[DEBUG LEXER] includes avant :", instructions, "liste modules inclus:", self.liste_included)
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
        if self.debug : print("[DEBUG LEXER] includes apres :", instructions, "liste modules inclus:", self.liste_included)
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
        if self.debug : print(f"[DEBUG LEXER] macros avant (iteration {globals()['iteration']}) :", content)
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
        if self.debug : print(f"[DEBUG LEXER] macros pendant (iteration {globals()['iteration']}) : macros:{macros_total}, content:{content}")
        content_remplacement = []
        for item in content:
            for macro in macros_total:
                if macro[0] == item:
                    content_remplacement += macro[1]
            if not sum(macro[0] == item for macro in macros_total):
                content_remplacement.append(item)
        content = content_remplacement
        if self.debug : print(f"[DEBUG LEXER] macros après (iteration {globals()['iteration']}) :", content)
        if sum([macro[0] == content[i] for macro in macros_total for i in range(len(content))]):
            self.total_macros += 1
            self.check_for_infinite_loop()
            content = self.parse_macros(content, macros_total)
        return content