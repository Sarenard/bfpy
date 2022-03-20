from src.Instructions import I1, Types

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
            if instruction.isnumeric():
                self.instructions.append((I1.PUSHINT, int(instruction), ))
            elif instruction == "set":
                self.instructions.append((I1.SET, ))
            else:
                self.instructions.append((I1.PUSHSTR, instruction, ))


            instruction_index += 1
        
        if self.debug : print("[DEBUG LEXER] instructions :", self.instructions)
        

    def add_instructions(self, instructions):
        self.instructions += instructions
        
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