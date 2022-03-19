import subprocess
from subprocess import Popen, PIPE, STDOUT

def test(file):
    proc = Popen(file.name.split(' '), stdout=PIPE, stderr=PIPE)
    (output, error) = proc.communicate()
    if error != file.espected_error:
        print(f"Error not conform in {file.name}, espected {file.espected_error}, got {error}")
    if output != file.espected_output:
        print(f"Output not conform in {file.name}, espected {file.espected_output}, got {output}")
    if output == file.espected_output and error == file.espected_error:
        print(f"Test {file.name} passed")
    return (output, error)

class File:
    def __init__(self, name, espected_output=b'', espected_error=b'', input=b''):
        self.name = f"python main.py -f exemples/{name}"
        self.espected_output  = espected_output
        self.espected_error   = espected_error
        self.input            = input
    

files_to_test = [
    File("add.bfr", b"5", b''),
    File("doubler.bfr", b"6", b''),
    File("hello_world.bfr", b"Hello World !\r\n", b''),
    File("equal.bfr", b"resultat : 1\r\n", b''),
    File("if_statement0.bfr", b"", b''),
    File("if_statement1.bfr", b"IN THE IF!", b''),
]
for file in files_to_test:
    test(file)