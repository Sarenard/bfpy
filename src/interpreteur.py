import sys

MAX_SIZE = 255 # DO NOT CHANGE

def simplify(code):
    code = code.replace("[-]", "a")
    code = code.replace("+[-<+]-", "b")
    code = code.replace("+++[--->+++]---", "c")
    return code

def interpreter(code, debug):
    code = ''.join(filter(lambda x: x in ".,[]<>+-", list(code)))
    code = simplify(code)
    bracemap = buildbracemap(code)
    cells, codeptr, cellptr = [0], 0, 0
    while codeptr < len(code):
        command = code[codeptr]
        if command == "+":
            cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < MAX_SIZE else 0
        elif command == "-":
            cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else MAX_SIZE
        elif command == "<":
            cellptr = 0 if cellptr <= 0 else cellptr - 1
        elif command == ">":
            cellptr += 1
            if cellptr == len(cells):
                cells.append(0)
        elif command == "[" and cells[cellptr] == 0:
            codeptr = bracemap[codeptr]
        elif command == "]" and cells[cellptr] != 0:
            codeptr = bracemap[codeptr]
        elif command == ",":
            cells[cellptr] = ord(input())
        elif command == ".":
            sys.stdout.write(chr(cells[cellptr]))
        elif command == "a":
            cells[cellptr] = 0
        elif command == "b":
            cellptr = 0
        elif command == "c":
            cellptr = 10+2
        codeptr += 1
        if debug : print("[INTERPRETATION] :", cells, f"pointer sur {cellptr}")

def buildbracemap(code):
    temp_bracestack, bracemap = [], {}
    for position, command in enumerate(code):
        if command == "[":
            temp_bracestack.append(position)
        elif command == "]":
            start = temp_bracestack.pop()
            bracemap[start] = position
            bracemap[position] = start
    return bracemap