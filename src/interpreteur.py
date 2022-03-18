import sys

def interpreter(code, debug):
    code = ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], list(code)))
    bracemap = buildbracemap(code)
    cells, codeptr, cellptr = [0], 0, 0
    while codeptr < len(code):
        if debug : print("[INTERPRETATION] :", cells, f"pointer sur {cellptr}")
        command = code[codeptr]
        if command == ">":
            cellptr += 1
            if cellptr == len(cells): cells.append(0)
        if command == "<":
            cellptr = 0 if cellptr <= 0 else cellptr - 1
        if command == "+":
            cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0
        if command == "-":
            cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255
        if command == "[" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
        if command == "]" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
        if command == ".": sys.stdout.write(chr(cells[cellptr]))
        if command == ",": cells[cellptr] = ord(input())
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