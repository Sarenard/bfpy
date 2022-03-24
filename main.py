# python .\main.py -f .\input.bfr -r
# python .\main.py -f .\input.bfr -toc -runcc

# TODO : LISTS

from src.generator import Generator
from src.lexer import Lexer
import argparse
import time
import os

parser = argparse.ArgumentParser(description='Interpreteur de code')
parser.add_argument('-f', '--file', help='fichier à interpreter', required=True)
parser.add_argument('-d', '--debug', help='mode debug', required=False, action='store_true')
parser.add_argument('-di', '--debuginterpreteur', help='mode debug', required=False, action='store_true')
parser.add_argument('-rc', '--runc', help='mode debug', required=False, action='store_true')
parser.add_argument('-rp', '--runp', help='mode debug', required=False, action='store_true')
parser.add_argument('-r', '--run', help='mode debug', required=False, action='store_true')
parser.add_argument('-stfu', '--stfu', help='mode debug', required=False, action='store_true')
args = parser.parse_args()

code = ("\n".join([x for x in open(args.file).read().split("\n") if not x.strip().startswith("//")]).replace("\n", " ")+" main").split(" ")

if not args.stfu : print("[INFO] : Génération du code")
t = time.time()
lexer = Lexer(args.debug)
lexer.parse(code)
instructions = lexer.instructions
generator = Generator(args.debug)
generator.generate(instructions)
instructions = generator.instructions
with open("sortie.bf", "w") as f:
    f.write(instructions)
if not args.stfu : print(f"[INFO] : Génération du code terminée en {time.time() - t} secondes")

if not args.stfu : print("[INFO] : Execution du code")

t = time.time()
if args.runc:
    os.system(".\src\interpreteur.exe .\sortie.bf")
if args.runp:
    from src.interpreteur import interpreter
    interpreter(instructions, args.debuginterpreteur)
if args.run:
    longueur = len(instructions)
    if longueur > 10000:
        os.system(".\src\interpreteur.exe .\sortie.bf")
    else:
        from src.interpreteur import interpreter
        interpreter(instructions, args.debuginterpreteur)
        
if not args.stfu : print(f"[INFO] : Execution du code terminée en {time.time() - t} secondes")