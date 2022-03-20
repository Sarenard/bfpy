from subprocess import Popen, PIPE

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
        self.name = f"python main.py -f exemples/{name} -rp -stfu"
        self.espected_output  = espected_output
        self.espected_error   = espected_error
        self.input            = input

files_to_test = [
    File("Helloworld.bfr", b"Hello World !\r\n", b''),
    File("if0.bfr", b"Hello World 1\r\n", b''),
    File("if1.bfr", b"Hello World 2\r\n", b''),
    File("loop.bfr", b"Hello World !\r\nHello World !\r\nHello World !\r\nHello World !\r\nHello World !\r\n", b''),
]
for file in files_to_test:
    test(file)