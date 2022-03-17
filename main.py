from src.interpreteur import interpreter
from src.generateur import Generateur
import argparse
# parse args
parser = argparse.ArgumentParser(description='Interpreteur de code')
parser.add_argument('-f', '--file', help='fichier à interpreter', required=True)
parser.add_argument('-d', '--debug', help='mode debug', required=False, action='store_true')
parser.add_argument('-di', '--debugi', help='mode debug interpreteur', required=False, action='store_true')
parser.add_argument('-ni', '--noti', help='mode non interprete', required=False, action='store_true')
args = parser.parse_args()

with open(args.file, 'r') as f:
    code = f.read()
    
generateur = Generateur(code, args.debug)
generateur.generate_instructions()

if not args.noti : interpreter(generateur.instructions, args.debugi)

if args.debug and not args.noti : print("[INFO] INTERPRETATION")

with open('sortie.bf', 'w', encoding="utf-8") as f:
    f.write(generateur.instructions)
