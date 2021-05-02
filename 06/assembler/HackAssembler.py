import sys
from Code import Code
from SymbolTable import SymbolTable
from Parser import Parser, CommandType


def main(file_name):
    assembler = HackAssembler(file_name)
    compiled_code = assembler.compile()
    print(compiled_code[5:])
    new_name = assembler.file_name.replace(".asm", ".hack")
    with open(new_name, "w") as writer:
        writer.write(compiled_code)


class HackAssembler:

    def __init__(self, file_name):
        self.file_name = file_name
        self.code = Code()
        self.symbol_table = SymbolTable(False)
        self.parser = Parser(file_name)

    def compile(self):
        compiled_code = ""
        while self.parser.has_more_commands():
            compiled_code += self.parser.current_line
            self.parser.advance()
        return compiled_code


if __name__ == '__main__':
    file_name = sys.argv[1]
    main(file_name)
