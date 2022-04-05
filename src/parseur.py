class Parseur:
    def __init__(self, debug):
        self.debug = debug
        self.instructions = []
        self.temp_string = ""
        self.string = False
    def parse(self, code):
        if self.debug : print("[DEBUG PARSEUR] : Parsing : "+code.replace("\n", "\\n"))
        code = code.replace("\n", " ")+" main"
        code = code.split(" ")
        x = 0
        while x < len(code):
            truc = code[x]
            if truc.strip().startswith("//") or truc == "":
                pass
            elif truc.startswith("\"") and not truc.endswith("\""):
                self.string = True
                self.temp_string += truc
            elif truc.endswith("\"") and not truc.startswith("\""):
                self.string = False
                self.temp_string += f" {truc}"
                self.instructions.append(self.temp_string)
                self.temp_string = ""
            elif truc.startswith("\"") and truc.endswith("\""):
                self.instructions.append(truc)
            elif self.string:
                self.temp_string += f" {truc}"
            else:
                if truc in ["-=", "+="]:
                    variable, integer, x = self.instructions.pop(), int(code[x+1]), x+1
                    if integer == 0:
                        pass
                    elif integer > 0:
                        self.instructions += [f"-{integer}", variable, "cadd"]
                    else:
                        self.instructions += [f"{integer}", variable, "cadd"]
                else:
                    self.instructions.append(truc)
            x += 1
        if self.debug : print(f"[DEBUG PARSEUR] : Parsing terminé {self.instructions}")
        return self.instructions