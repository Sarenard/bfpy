import sys

POWER = 8
OVERWRITE = 999
MAX_SIZE = max(2**POWER-1, OVERWRITE)

def interpreter(code, debug):
    code = ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-', 'D', 'S'], list(code)))
    bracemap = buildbracemap(code)
    cells, codeptr, cellptr = [0], 0, 0
    while codeptr < len(code):
        if debug : print("[INTERPRETATION] :", cells, f"pointer sur {cellptr}")
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
        if command == "[" and cells[cellptr] == 0:
            codeptr = bracemap[codeptr]
        if command == "]" and cells[cellptr] != 0:
            codeptr = bracemap[codeptr]
        if command == ",":
            cells[cellptr] = ord(input())
        elif command == ".":
            sys.stdout.write(chr(cells[cellptr]))
        if command == "D":
            debug = not debug
        if command == "S":
            print("[STOPPED] :", cells, f"pointer sur {cellptr}", f"len = {len(cells)}")
            sys.exit(1)
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

file = open("exemples/brainfuck/brainfuck.bf", "r").read()

interpreter(file, True)