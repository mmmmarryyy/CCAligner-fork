from subprocess import run
from tokenize import generate_tokens, untokenize, NUMBER, STRING, NAME, OP
import tokenize
from io import StringIO

AUTOPEP8_LOC = '/home/lokiplot/.local/bin/autopep8'

"""command = f'{AUTOPEP8_LOC} ../data/normalized_codebases/codebase1/ --recursive --in-place --pep8-passes 2000 --verbose'
command1 = 'which autopep8'
command2 = 'ls /home'
result = run(command, shell=True, capture_output=True, text=True)

if result.returncode == 0:
    print("Command executed successfully")
    print("Command output:")
    print(result.stdout)
else:
    print("Command failed")
    print("Error message:")
    print(result.stderr)"""

with open('../data/original_codebases/codebase1/b.py', 'r') as f:
    tokens = generate_tokens(f.readline)
    for line in f:
        print(line[0])

