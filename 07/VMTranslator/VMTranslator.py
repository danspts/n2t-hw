import sys
from Code import Code
from SymbolTable import SymbolTable
from Parser import Parser, CommandType
import re


def main(file_name):
    translator = VMTranslator(file_name)
    compiled_code = translator.delete_comments()
    compiled_code = translator.compile(compiled_code)
    print(compiled_code)
    new_name = translator.file_name.replace(".vm", ".asm")
    with open(new_name, "w") as writer:
        writer.write(compiled_code)


class VMTranslator:

    def __init__(self, file_name):
        self.file_name = file_name
        self.code = Code()
        self.symbol_table = SymbolTable()
        self.parser = Parser(file_name)
        self.label_index = 0
        self.compiled_code = ''

    def delete_comments(self):
        compiled_code = ""
        while self.parser.has_more_commands():
            compiled_code += self.parser.current_line
            self.parser.advance()
        return compiled_code

    def compile(self, code):
        code_lines = code.split('\n')
        for line in code_lines:
            if 'push constant' in line:
                # the line.strip()[-1] is to get the number in the end of the line
                self.push_constant(line.strip()[-1])
            elif 'pop local' in line:
                self.pop_local(line.strip()[-1])
            elif 'add' in line:
                self.calculate('+')
            elif 'sub' in line:
                self.calculate('-')
            elif 'neg' in line:
                self.negate_or_not('-')
            elif 'eq' in line:
                self.compare('JEQ')
            elif 'gt' in line:
                self.compare('JGT')
            elif 'lt' in line:
                self.compare('JLT')
            elif 'and' in line:
                self.calculate('&')
            elif 'or' in line:
                self.calculate('|')
            elif 'not' in line:
                self.negate_or_not('!')

        return self.compiled_code

    def push_constant(self, mem_index):
        # push constant i
        # pseudo code
        # RAM[SP] = constant i
        # SP++
        #
        # the number is always in the last index, strip for safety
        # D=i
        self.set_D_to_constant(mem_index)
        # RAM[SP] = D
        self.set_ram('SP', 'D')
        # SP++
        self.inc_sp()

    def pop_local(self, mem_index):
        # pop local i
        # pseudo code
        # D = pop x
        # SP--
        # RAM[addr] = RAM[SP]
        #
        # the number is always in the last index, strip for safety
        # addr <- LCL + i          D = LCL + i   ||   addr = D
        self.compiled_code += f'@LCL\nD=M\n@{mem_index}\nD=D+A\n@addr\nM=D\n'
        # SP--
        self.red_sp()
        # RAM[addr] = RAM[SP]
        # D = RAM[SP]
        self.get_ram('SP', 'D')
        # RAM[addr] = D
        self.set_ram('addr', 'D')

    def calculate(self, action):
        compiled_code = ''
        # SP--
        self.red_sp()
        # D = RAM[SP]
        self.get_ram('SP', 'D')
        # SP--
        self.red_sp()
        # A = RAM[SP]
        self.get_ram('SP', 'A')
        # action on A and D
        self.compiled_code += f'D=D{action}A\n'
        # RAM[SP] = D
        self.set_ram('SP', 'D')
        # SP++
        self.inc_sp()
        return compiled_code

    def negate_or_not(self, action):
        # SP--
        self.red_sp()
        # D = RAM[SP]
        self.get_ram('SP', 'D')
        # action on A and D
        self.compiled_code += f'D={action}D\n'
        # RAM[SP] = D
        self.set_ram('SP', 'D')
        # SP++
        self.inc_sp()

    def compare(self, con):
        # SP--
        self.red_sp()
        # D = RAM[SP]
        self.get_ram('SP', 'D')
        # SP--
        self.red_sp()
        # D = RAM[SP]
        self.get_ram('SP', 'A')
        # D=A-D
        self.compiled_code += 'D=A-D\n'
        self.label_index += 1
        label_t, label_f = f'label_comp_T_{self.label_index}', f'label_comp_F_{self.label_index}'
        # D;jump to label_comp_<index>
        self.compiled_code += f'@{label_t}\nD;{con}\n'
        # RAM[SP]=0
        self.set_ram('SP', '0')
        # 0;JMP to label_comp_<index>
        self.compiled_code += f'@{label_t}\n0;JMP\n'
        # (label_comp_T_<index>)
        self.compiled_code += f'({label_t})\n'
        # RAM[SP]=-1
        self.set_ram('SP', '-1')
        # (label_comp_f_<index>)
        self.compiled_code += f'({label_f})\n'
        # SP++
        self.inc_sp()

    def set_D_to_constant(self, constant):
        self.compiled_code += f'@{constant}\nD=A\n'

    def set_A_to_constant(self, constant):
        self.compiled_code += f'@{constant}\nD=A\n'

    def set_ram(self, pointer, reg):
        self.compiled_code += f'@{pointer}\nA=M\nM={reg}\n'

    def get_ram(self, pointer, reg):
        self.compiled_code += f'@{pointer}\nA=M\n{reg}=M\n'

    def inc_sp(self):
        self.compiled_code += '@SP\nM=M+1\n'

    def red_sp(self):
        self.compiled_code += '@SP\nM=M-1\n'


if __name__ == '__main__':
    # file_name = sys.argv[1]
    file_name = r'D:\CS\CS2\2\nand2tetris\n2t-hw\07\StackArithmetic\StackTest\StackTest.vm'
    main(file_name)
