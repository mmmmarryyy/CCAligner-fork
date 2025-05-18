import argparse


def define_args():
    parser = argparse.ArgumentParser(description='Finds code clones candidates')
    parser.add_argument('-from', '-codebase_loc', help='enter location of codebase', dest='codebase_loc', required=True)
    parser.add_argument('-l', help='specify language of database you want to analyse', dest='lang', required=True)
    parser.add_argument('--query_file', help='path to a single source file for which we want to find clones', dest='query_file', required=True)
    args = parser.parse_args()
    return args
