from Parser import CommandType
from SymbolTable import get_address, unary


class CodeWriter:

    def __init__(self, new_name):
        self.name = new_name[:-4]
        self.compiled_code = open(new_name, "w")
        self.label_index = 0

    def write(self, line):
        self.compiled_code.write(line + "\n")

    def push_D_to_stack(self):
        self.get_memory_from_pointer('SP')
        self.inc_sp()

    def pop_stack_to_D(self):
        self.dec_sp()
        self.get_memory_from_pointer()

    def write_push_pop(self, command, arg_1, index):
        address = get_address(arg_1)
        if arg_1 == 'constant':
            self.address(index)
        elif arg_1 == 'static':
            self.address(f"{self.name}.{index}")
        elif arg_1 in ['pointer', 'temp']:
            self.label(f'R{address + int(index)}')
        elif arg_1 in ['local', 'argument', 'this', 'that']:
            self.address(address)
            self.write('D=M')
            self.label(index)
            self.write('A=D+A')
        if command == "push":
            self.push(arg_1)
        elif command == "pop":
            self.pop()

    def pop(self):
        self.write('D=A')
        self.address('R15')
        self.write('M=D')
        self.pop_stack_to_D()
        self.get_memory_from_pointer('R15')

    def push(self, arg_1):
        if arg_1 == 'constant':
            self.write('D=A')
        else:
            self.write('D=M')
        self.push_D_to_stack()

    def compare(self, jump_cmd):
        # x - y -> we can then compare if == 0, > 0 or < 0
        self.write('D=M-D')

        # set the compare address and compare on true
        self.address(f"COMPARE_T_{self.label_index}")
        self.write(f'D;{jump_cmd}')
        self.set_A_to_stack()
        self.write('M=0')

        # Otherwise compare on false
        self.address(f"COMPARE_F_{self.label_index}")
        self.write('0;JMP')

        # True Label: continue
        self.label(f'COMPARE_T_{self.label_index}')
        self.set_A_to_stack()
        self.write('M=-1')

        # False label: skip
        self.label(f'COMPARE_F_{self.label_index}')

        # SP++
        self.inc_sp()
        self.label_index += 1

    def get_memory_from_pointer(self, pointer=None):
        if pointer:
            self.address(pointer)
        self.write('A=M')
        self.write('M=D')

    def set_A_to_stack(self):
        self.address('SP')
        self.write('A=M')

    def inc_sp(self):
        self.address("SP")
        self.write('M=M+1')

    def dec_sp(self):
        self.address("SP")
        self.write('M=M-1')

    def write_arithmetic(self, command):

        if command not in unary:
            self.pop_stack_to_D()

        self.dec_sp()
        self.set_A_to_stack()

        if 'add' == command:
            self.write('M=M+D')
        elif 'and' == command:
            self.write('M=M&D')
        elif 'or' == command:
            self.write('M=M|D')
        elif 'sub' == command:
            self.write('M=M-D')
        elif 'neg' == command:
            self.write('M=-M')
        elif 'not' == command:
            self.write('M=!M')
        elif 'eq' == command:
            self.jump('JEQ')
        elif 'gt' == command:
            self.jump('JGT')
        elif 'lt' == command:
            self.jump('JLT')
        self.inc_sp()

    def write_if(self, location, num_locals):


    def write_goto(self, location):
        self.label(location)
        self.write('0;JMP')

    def write_function(self, function_name, nb_locals):
        self.label(function_name)
        for i in range(nb_locals):
            self.push('constant')

    def write_return(self):
        # TODO HW8
        pass

    def write_call(self, function_name, num_args):
        # TODO HW8
        pass

    def label(self, label):
        self.write(f"({label})")

    def address(self, address):
        self.write(f"@{address}")

    def close(self):
        self.compiled_code.close()
