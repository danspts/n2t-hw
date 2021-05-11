import sys
from Code import Code
from SymbolTable import SymbolTable
from Parser import Parser, CommandType
import re



def main(file_name):
    assembler = HackAssembler(file_name)
    assembler.pre_process()
    assembler.add_symbols()
    assembler.replace_symbols()
    assembler.compile_to_machine_hack()


class HackAssembler:

    def __init__(self, file_name):
        self.file_name = file_name
        self.new_name = self.file_name.replace(".asm", ".hack")
        self.code = Code()
        self.symbol_table = SymbolTable()
        self.parser = Parser(file_name)

    def compile_to_machine_hack(self):
        self.parser = Parser(self.new_name)
        compiled_code = ""
        while self.parser.has_more_commands():

            if self.parser.command_type in [CommandType.A_COMMAND, CommandType.L_COMMAND]:
                compiled_code += self.to_bin(self.parser.symbol()) + "\n"
            else:
                comp = self.parser.comp()
                dest = self.parser.dest()
                jump = self.parser.jump()
                c_command = f"111{self.code.comp(comp)}{self.code.dest(dest)}{self.code.jump(jump)}"
                compiled_code += c_command + "\n"
            self.parser.advance()

        self.write(compiled_code)

    @staticmethod
    def to_bin(number):
        binary = bin(int(number))[2:]
        add_zero = 16 - len(binary)
        return add_zero * '0' + binary

    def write(self, input):
        with open(self.new_name, "w") as writer:
            writer.write(input)

    def pre_process(self):
        compiled_code = ""
        while self.parser.has_more_commands():
            if self.parser.current_line != "\n":
                compiled_code += self.parser.current_line
            self.parser.advance()
        self.write(compiled_code)

    def add_symbols(self):

        #Substitutes the lables first
        self.parser = Parser(self.new_name)
        compiled_code = ""
        while self.parser.has_more_commands():
            if self.parser.command_type == CommandType.L_COMMAND:
                address = self.symbol_table.get_program_address()
                symbol = self.parser.symbol()
                self.symbol_table.add_entry(symbol, address)
            else:
                compiled_code += self.parser.current_line
                self.symbol_table.increment_address()
            self.parser.advance()
        self.write(compiled_code)

        #Substitutes the first instance of
        self.parser = Parser(self.new_name)
        compiled_code = ""
        while self.parser.has_more_commands():
            if self.parser.command_type == CommandType.A_COMMAND:
                symbol = self.parser.symbol().strip()
                if not self.symbol_table.contains(symbol) and not symbol.isdigit():
                    address = self.symbol_table.get_data_address()
                    self.symbol_table.add_entry(symbol, address)
                    compiled_code += f"@{address}\n"
                    self.symbol_table.increment_data_address()
                else:
                    compiled_code += self.parser.current_line

            else:
                compiled_code += self.parser.current_line
            self.parser.advance()
        self.write(compiled_code)

    def replace_symbols(self):
        self.parser = Parser(self.new_name)
        compiled_code = ""
        while self.parser.has_more_commands():
            if self.parser.command_type == CommandType.A_COMMAND:
                symbol = self.parser.symbol().strip()
                symbol = symbol if symbol.isdigit() else self.symbol_table.get_address(symbol)
                compiled_code += f"@{symbol}\n"
            else:
                compiled_code += self.parser.current_line
            self.parser.advance()
        self.write(compiled_code)


if __name__ == '__main__':
    file_name = sys.argv[1]
    main(file_name)
