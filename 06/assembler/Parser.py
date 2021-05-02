from enum import Enum
from re import compile


class CommandType(Enum):
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2


class Parser:
    reg_command_split = compile("([MDA]{1,2})\s*=\s*([1&|M!0D+A-]*)")
    reg_jump_split = compile("([MDA+0-1]{1,2})\s*;\s*(\S*)")
    reg_format = compile("([^/]*)")

    def __init__(self, file=None):
        self.reader = open(file, 'r')
        self.__current_line = ""
        self.advance()

    def advance(self):
        read = self.reader.readline()
        current_line = Parser.reg_format.findall(read)
        self.__current_line = current_line[0].strip()
        if self.__current_line[:2] == "//" or (read and not self.__current_line):
            self.advance()

    def has_more_commands(self):
        return self.__current_line != ""

    @property
    def current_line(self):
        return self.__current_line + "\n"

    @property
    def command_type(self):
        if self.__current_line[0] == '@':
            return CommandType.A_COMMAND
        elif self.__current_line[0] == '(' and self.__current_line[-1] == ')':
            return CommandType.L_COMMAND
        else:
            return CommandType.C_COMMAND

    def symbol(self):
        if self.command_type == CommandType.A_COMMAND:
            return self.current_line[1:]
        elif self.command_type == CommandType.L_COMMAND:
            return self.current_line[1:-2]
        else:
            raise ValueError

    def dest(self):
        result = Parser.reg_command_split.findall(self.current_line)
        if result:
            return result[0][0]
        else:
            return 'NULL'

    def comp(self):
        result_comm = Parser.reg_command_split.findall(self.current_line)
        result_jump = Parser.reg_jump_split.findall(self.current_line)
        if result_comm:
            return result_comm[0][1]
        elif result_jump:
            return result_jump[0][0]
        else:
            return 'NULL'

    def jump(self):
        result = Parser.reg_jump_split.findall(self.current_line)
        if result:
            return result[0][1]
        else:
            return 'NULL'
