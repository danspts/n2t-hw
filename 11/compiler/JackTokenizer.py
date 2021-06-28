from enum import Enum
import re


class Types(Enum):
    KEYWORD = 0
    SYMBOL = 1
    IDENTIFIER = 2
    INT_CONST = 3
    STRING_CONST = 4


class VariableType(Enum):
    INT = 0
    CHAR = 1
    BOOLEAN = 2
    CLASS_NAME = 3


class VariableKind(Enum):
    FIELD = 0
    STATIC = 1
    LOCAL = 2
    ARGUMENT = 3


class VariableScope(Enum):
    SUBROUTINE = 0
    CLASS = 1


class VariableInfo:
    def __init__(self):
        self.type = None
        self.kind = None
        self.running_index = -1
        self.scope = None

    def set_kind(self, string):
        if string == 'var':
            self.kind = VariableKind.LOCAL
        elif string == 'argument':
            self.kind = VariableKind.ARGUMENT
        elif string == 'field':
            self.kind = VariableKind.FIELD
        elif string == 'static':
            self.kind = VariableKind.STATIC
        else:
            self.kind = string

    def set_type(self, string):
        if string == 'var':
            self.type = VariableType.INT
        elif string == 'argument':
            self.type = VariableType.CHAR
        elif string == 'field':
            self.type = VariableType.BOOLEAN
        elif type(string) == str:
            self.type = VariableType.CLASS_NAME
        else: # if its a number so its already defined put it here
            self.type = string

    def set_index(self, index):
        self.running_index = index

    def set_scope(self, string):
        self.scope = string

class Token:
    def __init__(self, string, token_type):
        self.string = string
        self.token_type = token_type
        self.is_variable = False
        self.variable_info = VariableInfo()


class JackTokenizer:
    def __init__(self, file_name):
        self.symbols_list = list("{}()[].,;+-*/&|<>=~")
        self.symbols_regex_string = r"\{|}|\(|\)|\[|]|\.|,|;|\+|-|\*|/|&|\||<|>|=|~| |"
        self.keywords_list = "class constructor function method field static var int char boolean void true false null this let do if else while return" \
            .split(" ")

        self.tokens = []
        self.reader = open(file_name, 'r')
        self.parse()
        self.index = 0
        self.number = None
        self.identifier = None
        self.reset_num = False
        self.reset_identifier = False

    def reset(self):
        # reset number and identifiers becuase there was a white space
        if self.number is not None:
            self.tokens.append(Token(self.number, token_type=Types.INT_CONST))
        self.number = None
        self.reset_num = False
        if self.identifier is not None:
            self.tokens.append(Token(self.identifier, token_type=Types.IDENTIFIER))
        self.identifier = None
        self.reset_identifier = False

    def tokenize_line(self, line):
        # split keywords, white space and symbols
        regex_split = re.split(f"({self.symbols_regex_string + ' | '.join(self.keywords_list)})", line)
        string_const = None
        for string in regex_split:
            if string.strip() != '':
                string = string.strip()

                # edge case if there is a white space in a string const
                if string_const is not None:
                    if string[-1] == '"':
                        string_const += ' ' + string[:-1]
                        self.tokens.append(Token(string_const, token_type=Types.STRING_CONST))
                        string_const = None
                    else:
                        string_const += ' ' + string
                    continue

                if string in self.keywords_list:
                    self.tokens.append(Token(string, token_type=Types.KEYWORD))
                elif string in self.symbols_list:
                    self.tokens.append(Token(string, token_type=Types.SYMBOL))
                elif string.isnumeric():
                    self.tokens.append(Token(string, token_type=Types.INT_CONST))
                elif string[0] == '"':
                    # regex split the with space in the string constant
                    if string[-1] == '"':
                        self.tokens.append(Token(string[1:-1], token_type=Types.STRING_CONST))
                    else:
                        string_const = string[1:]
                else:
                    self.tokens.append(Token(string, token_type=Types.IDENTIFIER))

    def parse(self):
        read = self.reader.readline()
        while read != '':
            if '/**' in read:
                read = self.reader.readline()
                if read.strip() != "":
                    while read.strip()[0] == '*':
                        read = self.reader.readline()
                        if read.strip() == '':
                            break

            if read.split('//')[0].strip() != '' and "/**" not in read:
                self.tokenize_line(read.split('//')[0].strip())
            read = self.reader.readline()

    def advance(self):
        token = self.tokens[self.index]
        self.index += 1
        return token

    def has_more_tokens(self):
        return self.index < len(self.tokens)
