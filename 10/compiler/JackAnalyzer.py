import sys
from os import listdir
from JackTokenizer import *
from CompilationEngine import *


def tokenize_file(file_name):
    tokens = JackTokenizer(file_name)
    with open(file_name.replace('.jack', 'test.xml'), "w") as writer:
        compilation_engine = CompilationEngine(tokens, writer)


def dir_or_file(argument):
    if argument[-5:] == ".jack":
        tokenize_file(argument)
    else:
        for file in listdir(argument)[::-1]:
            if file[-5:] == ".jack":
                tokenize_file(f"{argument}/{file}")


if __name__ == '__main__':
    if len(sys.argv) > 2:
        print("Usage: python JackAnalyzer {file_name | directory_name}")
    elif len(sys.argv) == 1:
        dir_or_file(".")
    else:
        file_name = sys.argv[1]
        dir_or_file(file_name)
