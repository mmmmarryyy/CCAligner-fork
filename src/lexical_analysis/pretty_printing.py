from subprocess import run
from shutil import copytree
import tokenize
import glob
import os
from tree_sitter import Language, Parser
from lexical_analysis.obfuscation import Obfuscator


AUTOPEP8_LOC = '/home/lokiplot/.local/bin/autopep8'

Language.build_library(
  # Store the library in the `build` directory
  '../build/my-languages.so',

  # Include one or more languages
  [
    'tree-sitter-python',
    'tree-sitter-java'
  ]
)



class PrettyPrinter(object):
    def __init__(self, codebase_loc: str, pretty_loc: str, language: str):
        self.language = language
        self.lang_ext = None

        if self.language == 'python':
            self.lang_ext = '.py'
        elif self.language == 'java':
            self.lang_ext = '.java'
        self._codebase_loc = codebase_loc
        self._pretty_codebase_loc = pretty_loc + self._codebase_loc.split('/')[-1]
        os.makedirs(self._pretty_codebase_loc, exist_ok=True)
        self._without_type1_changes_loc = self._pretty_codebase_loc + "/type1_normalized"
        self._pep8_loc = self._pretty_codebase_loc + "/pep8"
        self._codeblocks_loc = self._pretty_codebase_loc + "/codeblocks"
        self._obfuscated_loc = self._pretty_codebase_loc + "/obfuscated"
        self.tree = None  # will contain new tree-sitter tree for every file in codebase
        self.cursor = None  # will contain tree's cursor


    @staticmethod
    def remove_type1_changes_file(file_loc, new_loc):
        new_file_name = new_loc + '/' + file_loc.split('/')[-1]  # can create collision
        new_file_content = list()
        prev_token_type = tokenize.INDENT
        last_lineno = -1
        last_col = 0
        line = ""
        with open(file_loc, 'r') as f:
            tokens = tokenize.generate_tokens(f.readline)
            for token in tokens:
                token_type = token[0]
                token_string = token[1]
                start_line, start_col = token[2]
                end_line, end_col = token[3]
                if start_line > last_lineno:
                    if line.strip() != "":
                        new_file_content.append(line)
                    line = ""
                    last_col = 0
                if start_col > last_col:
                    line += (" " * (start_col - last_col))
                if token_type == tokenize.COMMENT:
                    pass
                elif token_type == tokenize.STRING or token_type == tokenize.NUMBER:
                    if prev_token_type not in [tokenize.INDENT, tokenize.NEWLINE]:
                        if start_col > 0:
                            line += token_string
                else:
                    line += token_string
                prev_token_type = token_type
                last_col = end_col
                last_lineno = end_line

        # TODO: обработать правильно переносы строки () и expressions, которые ничего не делают

        nf = open(new_file_name, 'w')
        nf.write(''.join(new_file_content))
        nf.close()

    def remove_type1_changes_in_codebase(self):
        os.mkdir(self._without_type1_changes_loc)
        for file in glob.glob(self._pep8_loc + "/**/*" + self.lang_ext, recursive=True):
            self.remove_type1_changes_file(file, self._without_type1_changes_loc)
        return True

    def to_pep8_and_copy_codebase(self) -> bool:
        """
        copies original codebase to new directory (creates new_loc dir) and transforms it to pep8
        respects codebase_dir structure
        :param self:
        :return: True if command was successful
        """
        copytree(self._codebase_loc, self._pep8_loc)
        command_to_pep8 = f'{AUTOPEP8_LOC} {self._pep8_loc} --recursive --in-place --pep8-passes 2000 --verbose'
        status = run(command_to_pep8, shell=True, capture_output=True, text=True).returncode
        return status == 0

    @staticmethod
    def copy_code_fragment(file_loc: str, file_dest: str, start_line, end_line):
        """
        we will pass only starting lines, because after normalization codeblock can not
        end or start in the middle of the line
        :param file_loc:
        :param file_dest:
        :param start_line:
        :param end_line:
        :return:
        """
        with open(file_loc, 'r') as source_file:
            lines = source_file.readlines()
        code_fragment_lines = lines[start_line: end_line + 1]
        number_of_indents = len(code_fragment_lines[0]) - len(code_fragment_lines[0].lstrip())
        code_fragment_lines = [line[number_of_indents:] for line in code_fragment_lines]
        extracted_code = ''.join(code_fragment_lines)
        with open(file_dest, 'w') as destination_file:
            destination_file.write(extracted_code)

    def finding_blocks(self, node, storing_loc, file_loc):
        if len(node.children) == 0:
            return
        if node.type == 'block':
            start_line = node.start_point[0]
            end_line = node.end_point[0]
            codeblock_file_name = f'{storing_loc}/{start_line + 1}_{end_line + 1}{self.lang_ext}'
            self.copy_code_fragment(file_loc, codeblock_file_name, start_line, end_line)
        for child in node.children:
            self.finding_blocks(child, storing_loc, file_loc)

    def split_to_codeblocks_file(self, file_loc, new_loc):
        parser = Parser()
        language = Language('../build/my-languages.so', self.language)
        parser.set_language(language)
        with open(file_loc, "rb") as f:
            content = f.read()
        self.tree = parser.parse(content)
        storing_loc = new_loc + '/' + file_loc.split('/')[-1][:-1]
        os.mkdir(storing_loc)
        root_node = self.tree.root_node
        self.finding_blocks(root_node, storing_loc, file_loc)

    def split_to_codeblocks_codebase(self):
        os.mkdir(self._codeblocks_loc)
        for file in glob.glob(self._without_type1_changes_loc + "/**/*" + self.lang_ext, recursive=True):
            self.split_to_codeblocks_file(file, self._codeblocks_loc)
        return True

    def obfuscate_codebase(self):
        os.mkdir(self._obfuscated_loc)
        for file in glob.glob(self._codeblocks_loc + "/**/*" + self.lang_ext, recursive=True):
            same_dir = self._obfuscated_loc + '/' + file.split('/')[-2]
            if not os.path.exists(same_dir):
                os.mkdir(same_dir)
            ob = Obfuscator(file, same_dir, self.language)
            ob.obfuscate()
        return True

    def pretty_print(self):
        if self.to_pep8_and_copy_codebase():
            print("Brought into proper style")
        if self.remove_type1_changes_in_codebase():
            print("Removed type 1 changes")
        if self.split_to_codeblocks_codebase():
            print("Split to codeblocks")
        if self.obfuscate_codebase():
            print("Obfuscated")


