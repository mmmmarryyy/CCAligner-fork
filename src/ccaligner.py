import lexical_analysis.pretty_printing as prpr
from launching import define_args
from subprocess import run


args = define_args()

codebase_loc = args.codebase_loc

pretty_loc = "./data/normalized_codebases/"

pp = prpr.PrettyPrinter(codebase_loc, pretty_loc)
pp.pretty_print()
