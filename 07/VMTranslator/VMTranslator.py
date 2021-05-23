import sys
from CodeWriter import CodeWriter
from Parser import Parser, CommandType
from os import listdir
import re



def main(file_name):
    translator = VMTranslator(file_name)
    translator.translate()


class VMTranslator:

    get_dirname_re = re.compile(".*/(.*?)/?$")

    def __init__(self, file_name):
        self.file_name = file_name.replace(".vm", ".asm")
        self.parser = Parser(file_name)
        self.code = CodeWriter(self.file_name)

    def translate(self):
        # self.code.write_init()
        while self.parser.has_more_commands():
            print(self.parser.command, self.parser.arg_1, self.parser.arg_2)
            self.write()
            self.parser.advance()
        self.code.close()

    def write(self):
        cmd = self.parser.command_type()
        print(cmd)
        # HW7
        if cmd == CommandType.C_ARITHMETIC:
            self.code.write_arithmetic(self.parser.command)
        if cmd in [CommandType.C_PUSH, CommandType.C_POP]:
            self.code.write_push_pop(self.parser.command, self.parser.arg_1, self.parser.arg_2)
        elif cmd == CommandType.C_LABEL:
            self.code.label(self.parser.arg_1)
        # HW8
        elif cmd == CommandType.C_GOTO:
            self.code.write_goto(self.parser.arg_1)
        elif cmd == CommandType.C_IF:
            self.code.write_if(self.parser.arg_1)
        elif cmd == CommandType.C_FUNCTION:
            self.code.write_function(self.parser.arg_1, self.parser.arg_2)
        elif cmd == CommandType.C_RETURN:
            self.code.write_return()
        elif cmd == CommandType.C_CALL:
            self.code.write_call(self.parser.arg_1, self.parser.arg_2)


def dir_or_file(argument):
    if argument[-3:] == ".vm":
        main(argument)
    else:
        # turn all vm files to asm
        for file in listdir(argument):
            if file[-3:] == ".vm":
                main(f"{argument}/{file}")
        # concatenates all asm files
        with open(f"{argument}/{VMTranslator.get_dirname_re.findall(argument)[0]}.asm", "w") as writer:
            for file in listdir(argument):
                if file[-4:] == ".asm":
                    writer.write(open(f"{argument}/{file}", "r").read())


if __name__ == '__main__':
    if len(sys.argv) > 2:
        print(f"Usage: python VMTranslator {{file_name, directory_name}}")
    elif len(sys.argv) == 1:
        dir_or_file(".")
    else:
        file_name = sys.argv[1]
        dir_or_file(file_name)
