from enum import Enum
from re import compile


class CommandType(Enum):
    C_ARITHMETIC = 0
    C_PUSH = 1
    C_POP = 2
    C_LABEL = 3
    C_GOTO = 4
    C_IF = 5
    C_FUNCTION = 6
    C_RETURN = 7
    C_CALL = 8


class Parser:
    reg_format = compile("([^/]*)")
    reg_args = compile("(\S*)\s*(\S*)\s*(\S*)")

    _commands = {
        'gt': CommandType.C_ARITHMETIC,
        'not': CommandType.C_ARITHMETIC,
        'lt': CommandType.C_ARITHMETIC,
        'add': CommandType.C_ARITHMETIC,
        'or': CommandType.C_ARITHMETIC,
        'eq': CommandType.C_ARITHMETIC,
        'and': CommandType.C_ARITHMETIC,
        'sub': CommandType.C_ARITHMETIC,
        'neg': CommandType.C_ARITHMETIC,
        'label': CommandType.C_LABEL,
        'goto': CommandType.C_GOTO,
        'if-goto': CommandType.C_IF,
        'push': CommandType.C_PUSH,
        'pop': CommandType.C_POP,
        'call': CommandType.C_CALL,
        'return': CommandType.C_RETURN,
        'function': CommandType.C_FUNCTION
    }

    def __init__(self, file=None):
        self.reader = open(file, 'r')
        self.__current_line = ""
        self.command = ""
        self.arg_1 = ""
        self.arg_2 = ""
        self.advance()

    def advance(self):
        read = self.reader.readline()
        current_line = Parser.reg_format.findall(read)
        self.__current_line = current_line[0].strip()
        if self.__current_line[:2] == "//" or (read and not self.__current_line):
            self.advance()
        else:
            self.set_args()

    def has_more_commands(self):
        return self.__current_line != ""

    @property
    def current_line(self):
        return self.__current_line + "\n"

    def command_type(self):
        return self._commands[self.command]

    def set_args(self):
        arguments = Parser.reg_args.findall(self.__current_line)
        if arguments:
            self.command = arguments[0][0]
            self.arg_1 = arguments[0][1]
            self.arg_2 = arguments[0][2]
        else:
            self.command = self.__current_line
            self.arg_1 = ""
            self.arg_2 = ""
