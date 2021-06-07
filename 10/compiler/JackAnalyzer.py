import sys
from os import listdir
from JackTokenizer import *
from CompilationEngine import *


def tokenize_file(file_name):
    tokens = JackTokenizer(file_name)
    with open(file_name.replace('.jack', 'test.xml'), "w") as writer:
        compilation_engine = CompilationEngine(tokens, writer)
        # writer.write('<tokens>\n')
        # while tokens.has_more_tokens():
        #     token = tokens.advance()
        #     # special chars of xml
        #     if token.string == '<':
        #         token.string = '&lt'
        #     elif token.string == '>':
        #         token.string = '&gt'
        #     elif token.string == '"':
        #         token.string = '&quot'
        #     elif token.string == '&':
        #         token.string = '&amp'
        #
        #     if token.token_type == Types.SYMBOL:
        #         token.token_type = "symbol"
        #     elif token.token_type == Types.KEYWORD:
        #         token.token_type = "keyword"
        #     elif token.token_type == Types.IDENTIFIER:
        #         token.token_type = "identifier"
        #     elif token.token_type == Types.STRING_CONST:
        #         token.token_type = "stringConstant"
        #     elif token.token_type == Types.INT_CONST:
        #         token.token_type = "integerConstant"
        #
        #     line = f"<{token.token_type}> {token.string} </{token.token_type}>"
        #     print(line)
        #     writer.write(line + '\n')
        # writer.write('</tokens>\n')


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
