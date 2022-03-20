# python .\main.py -f .\input.bfr -ni --interpreter_in_c -r -c -cr

from src.interpreteur import interpreter
from src.generateur import Generateur
import argparse
import time
import os

# parse args
parser = argparse.ArgumentParser(description='Interpreteur de code')
parser.add_argument('-f', '--file', help='fichier à interpreter', required=True)
parser.add_argument('-d', '--debug', help='mode debug', required=False, action='store_true')
parser.add_argument('-c', '--compile', help='compiled in c', required=False, action='store_true')
parser.add_argument('-cr', '--compile_and_run', help='compiled in c', required=False, action='store_true')
parser.add_argument('-di', '--debugi', help='mode debug interpreteur', required=False, action='store_true')
parser.add_argument('-ni', '--noti', help='mode non interprete', required=False, action='store_true')
parser.add_argument('-ic', '--interpreter_in_c', help='mode non interprete', required=False, action='store_true')
parser.add_argument('-r', '--raw', help='raw mode', required=False, action='store_false')
args = parser.parse_args()

total = time.time()

with open(args.file, 'r') as f:
    code = f.read()
    
if not args.raw : print("[INFO] Début de la génération des instructions")
t = time.time()
generateur = Generateur(code, args.debug)
generateur.generate_instructions()
if not args.raw : print(f"[INFO] Instructions générées en {time.time()-t}s")

clean_bf = "".join([x for x in generateur.instructions if x in ['+', '-', '<', '>', '.', ',', '[', ']']])

if args.debug and not args.noti : print("[INFO] INTERPRETATION")
if args.debug and not args.noti : print(f"[INFO] instructions : {clean_bf}")

with open('sortie.bf', 'w', encoding="utf-8") as f:
    f.write(generateur.instructions)

if not args.noti : 
    if not args.raw : print("[INFO] Début de l'interprétation")
    t = time.time()
    interpreter(generateur.instructions, args.debugi)
    if not args.raw : print(f"[INFO] Interprété en {time.time()-t}s")

if args.interpreter_in_c:
    print("[INFO] Interpretation en C")
    t = time.time()
    os.system(f"src\interpreteur.exe sortie.bf")
    print(f"[INFO] Interprété en {time.time()-t}s")

if args.compile:
    print("[INFO] Compilation en C")
    t = time.time()
    os.system("python src/bftoc.py sortie.bf")
    os.system("gcc -o sortie sortie.c")
    print(f"[INFO] Compilé en {time.time()-t}s")
    
if args.compile_and_run:
    print("[INFO] Lancement du code en C")
    t = time.time()
    os.system("sortie.exe")
    print(f"[INFO] Exécuté en {time.time()-t}s")
    
if not args.raw : print(f"[INFO] Temps total : {time.time()-total}s")