from src.parser import Parser
from src.generator import Generator
import argparse
import os

parser = argparse.ArgumentParser(description='Interpreteur de code')
parser.add_argument('-f', '--file', help='fichier à interpreter', required=True)
parser.add_argument('-d', '--debug', help='mode debug', required=False, action='store_true')
parser.add_argument('-r', '--run', help='mode debug', required=False, action='store_true')
args = parser.parse_args()

code = open(args.file).read().replace("\n", " ").split(" ")

parser = Parser(args.debug)
parser.parse(code)
instructions = parser.instructions
generator = Generator(args.debug)
generator.generate(instructions)
instructions = generator.instructions

with open("sortie.bf", "w") as f:
    f.write(instructions)

if args.run:
    os.system(".\src\interpreteur.exe .\sortie.bf")