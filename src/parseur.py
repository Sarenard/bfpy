class Parseur:
    def __init__(self, debug):
        self.instructions = []
        self.temp_string = ""
        self.string = False
    def parse(self, code):
        print(f"[DEBUG PARSEUR] : Parsing : {code}")
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
                self.temp_string += truc
                self.instructions.append(self.temp_string.replace(" ", "\\N"))
                self.temp_string = ""
            elif truc.startswith("\"") and truc.endswith("\""):
                self.instructions.append(truc.replace(" ", "\\N"))
            elif self.string:
                self.temp_string += f" {truc}"
            else:
                self.instructions.append(truc)
            
        print(f"[DEBUG PARSEUR] : Parsing terminé {self.instructions}")
        return self.instructions