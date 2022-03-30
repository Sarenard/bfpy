class Parseur:
    def __init__(self, debug):
        self.debug = debug
        self.instructions = []
        self.temp_string = ""
        self.string = False
    def parse(self, code):
        if self.debug : print("[DEBUG PARSEUR] : Parsing : "+code.replace("\n", "\\n"))
        code = code.replace("\n", " ")+" main"
        for truc in code.split(" "):
            adder = self.instructions
            if truc.strip().startswith("//"):
                continue
            elif truc == "":
                continue
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
                self.instructions.append(truc)
            
        if self.debug : print(f"[DEBUG PARSEUR] : Parsing terminé {self.instructions}")
        return self.instructions