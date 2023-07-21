import lexical_analysis.pretty_printing as prpr
from launching import define_args
from subprocess import run
import os
import filecmp
from clone_detection.algorithm import CCalignerAlgorithm

def find_same_content_files(directory):
    txt_files = []
    for root, _, files in os.walk(directory):
        txt_files.extend([os.path.join(root, file) for file in files if file.endswith(".py")])

    for i, file1 in enumerate(txt_files):
        for file2 in txt_files[i + 1:]:
            if filecmp.cmp(file1, file2):
                print(f"Files with the same content: {file1} and {file2}")


args = define_args()

codebase_loc = args.codebase_loc

pretty_loc = "./data/normalized_codebases/"

pp = prpr.PrettyPrinter(codebase_loc, pretty_loc)
pp.pretty_print()

final_dir = pretty_loc + codebase_loc.split('/')[-1] + '/' + 'obfuscated'

cca = CCalignerAlgorithm(final_dir, 3, 0)
pairs = cca.run_algo()
for file1, file2 in pairs:
    file_name1 = file1.split('/')[-2]
    file_name2 = file2.split('/')[-2]
    fragment1 = file1.split('/')[-1][:-2]
    fragment2 = file2.split('/')[-1][:-2]
    print(f"{file_name1} and {file_name2} contain codeclone in lines {fragment1} and {fragment2} respectively")