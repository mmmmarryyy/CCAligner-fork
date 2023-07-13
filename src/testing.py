from subprocess import run
from tokenize import generate_tokens, untokenize, NUMBER, STRING, NAME, OP
import tokenize
from io import StringIO


def remove_comments_and_docstrings(source):
    """
    Returns 'source' minus comments and docstrings.
    """
    io_obj = StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        ltext = tok[4]
        # The following two conditionals preserve indentation.
        # This is necessary because we're not using tokenize.untokenize()
        # (because it spits out code with copious amounts of oddly-placed
        # whitespace).
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        # Remove comments:
        if token_type == tokenize.COMMENT:
            pass
        # This series of conditionals removes docstrings:
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
        # This is likely a docstring; double-check we're not inside an operator:
                if prev_toktype != tokenize.NEWLINE:
                    # Note regarding NEWLINE vs NL: The tokenize module
                    # differentiates between newlines that start a new statement
                    # and newlines inside of operators such as parens, brackes,
                    # and curly braces.  Newlines inside of operators are
                    # NEWLINE and newlines that start new code are NL.
                    # Catch whole-module docstrings:
                    if start_col > 0:
                        # Unlabelled indentation means we're inside an operator
                        out += token_string
                    # Note regarding the INDENT token: The tokenize module does
                    # not label indentation inside of an operator (parens,
                    # brackets, and curly braces) as actual indentation.
                    # For example:
                    # def foo():
                    #     "The spaces before this docstring are tokenize.INDENT"
                    #     test = [
                    #         "The spaces before this string do not get a token"
                    #     ]
                    else:
                        out += token_string
                    prev_toktype = token_type
                    last_col = end_col
                    last_lineno = end_line
        return out


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

