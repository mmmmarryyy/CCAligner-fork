import argparse


def define_args():
    parser = argparse.ArgumentParser(description='Finds code clones candidates')
    parser.add_argument('-from', '-codebase_loc', help='enter location of codebase', dest='codebase_loc', required=True)
    args = parser.parse_args()
    return args
