import sys
from Code import Code
from SymbolTable import SymbolTable
from Parser import Parser, CommandType
import re


def main(file_name):
    assembler = HackAssembler(file_name)
    compiled_code = assembler.compile()
    compiled_code = assembler.address_init(compiled_code)
    compiled_code = assembler.parse_symbols(compiled_code)
    print(compiled_code)
    compiled_code = assembler.to_binary(compiled_code)
    new_name = assembler.file_name.replace(".asm", ".hack")
    with open(new_name, "w") as writer:
        writer.write(compiled_code)


class HackAssembler:

    def __init__(self, file_name):
        self.file_name = file_name
        self.code = Code()
        self.symbol_table = SymbolTable()
        self.parser = Parser(file_name)

    def compile(self):
        compiled_code = ""
        while self.parser.has_more_commands():
            compiled_code += self.parser.current_line
            self.parser.advance()
        return compiled_code

    def address_init(self, compiled_code):
        index = 0
        no_l_types = ""
        for line in compiled_code.split('\n'):
            if re.search('\((.+)\)', line):
                self.symbol_table.add_entry(line[1:-1], index)
            else:
                index += 1
                no_l_types += line + '\n'
        return no_l_types

    def parse_symbols(self, compiled_code):
        symbol_less = ""
        for line in compiled_code.split('\n'):
            if '@' in line:
                if line[1:].isnumeric():
                    # if not self.symbol_table.contains(line[1:]):
                    #     self.symbol_table.add_entry(line[1:], int(line[1:]))
                    symbol_less += line + '\n'
                else:
                    if self.symbol_table.contains(line[1:]):
                        symbol_less += f'@{self.symbol_table.get_address(line[1:])}\n'
                    else:
                        address = self.symbol_table.get_new_address()
                        self.symbol_table.add_entry(str(address), address)
                        symbol_less += f'@{address}\n'
            else:
                symbol_less += line + '\n'
        return symbol_less

    def to_binary(self, compiled_code):
        binary = ''
        for line in compiled_code.strip().split('\n'):
            if line[0] == '@':
                bin_num = str(bin(int(line[1:])))[2:]
                binary += (16 - len(bin_num)) * '0' + bin_num
            else:
                dest = 'NULL'
                jump = 'NULL'
                comp = line.split('=')
                if len(comp) == 2:
                    dest = comp[0]
                    comp = comp[1]
                else:
                    comp = comp[0]
                comp = comp.split(';')
                if len(comp) == 2:
                    jump = comp[1]
                comp = comp[0]
                binary += '111' + self.code.comp_dict[comp] + self.code.dest_dict[dest] + self.code.jump_dict[jump]
            if binary[-16:] == '0000000000010001':
                print('hi')

            binary += '\n'

        return binary


if __name__ == '__main__':
    file_name = sys.argv[1]
    main(file_name)
