from subprocess import run
from tokenize import generate_tokens, untokenize, NUMBER, STRING, NAME, OP
import tokenize
from io import StringIO
from os import mkdir
from tree_sitter import Language, Parser

AUTOPEP8_LOC = '/home/lokiplot/.local/bin/autopep8'


def print_all_blocks(file_loc):
  pass


Language.build_library(
  # Store the library in the `build` directory
  '../build/my-languages.so',

  # Include one or more languages
  [
    '../tree-sitter-python'
  ]
)

PY_LANGUAGE = Language('../build/my-languages.so', 'python')

parser = Parser()
parser.set_language(PY_LANGUAGE)

f = open("../data/database2/ds.py", "rb")

content = f.read()


tree = parser.parse(content)

cursor = tree.walk()
assert cursor.node.type == 'module'

root_node = tree.root_node

f = open("../data/original_codebases/codebase1/a.py", "r")

content = f.readlines()

print("".join(content))

