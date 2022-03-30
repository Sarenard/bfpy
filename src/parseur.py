class Parseur:
    def __init__(self, debug):
        self.instructions = ""
    def parse(self, code):
        print(f"[DEBUG PARSEUR] : Parsing : {code}")
        self.instructions = [x for x in ("\n".join([x for x in code.split("\n") if not x.strip().startswith("//")]).replace("\n", " ")+" main").split(" ") if x != ""]
        print(f"[DEBUG PARSEUR] : Parsing terminé {self.instructions}")
        return self.instructions