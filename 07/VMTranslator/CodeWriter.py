from Parser import CommandType
from SymbolTable import get_address, unary


class CodeWriter:

    def __init__(self, new_name):
        self.name = new_name[:-4]
        self.compiled_code = open(new_name, "w")
        self.bool_index = 0
        self.call_index = 0

    def write(self, line):
        self.compiled_code.write(line + "\n")

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
        self.copy_memory_to_address(None, 'R15')
        self.pop_D_from_stack()
        self.D_to_ram('R15')

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
        self.address(f"COMPARE_T_{self.bool_index}")
        self.write(f'D;{jump_cmd}')
        self.set_A_to_stack()
        self.write('M=0')

        # Otherwise compare on false
        self.address(f"COMPARE_F_{self.bool_index}")
        self.write('0;JMP')

        # True Label: continue
        self.label(f'COMPARE_T_{self.bool_index}')
        self.set_A_to_stack()
        self.write('M=-1')

        # False label: skip
        self.label(f'COMPARE_F_{self.bool_index}')

        # SP++
        self.inc_sp()
        self.bool_index += 1

    def push_D_to_stack(self):
        self.D_to_ram('SP')
        self.inc_sp()

    def pop_D_from_stack(self):
        self.dec_sp()
        self.D_from_ram()

    def D_to_ram(self, addr=None):
        if addr: self.address(addr)
        self.write("A=M")
        self.write(f"M=D")  # M[addr] = D

    def D_from_ram(self, addr=None):
        if addr: self.address(addr)
        self.write("A=M")
        self.write(f"D=M")  # D = M[addr]

    def copy_memory_to_address(self, copy_from=None, copy_to=None):
        if copy_from:
            self.address(copy_from)
        self.write('D=M')
        self.address(copy_to)
        self.write('M=D')  # M[copy_to] = M[copy_from]

    def set_int_to_memory(self, addr, value = None):
        if value:
            self.address(value)
        self.write('D=A')
        self.address(addr)
        self.write('M=D')  # M[addr] = value

    def set_A_to_stack(self):
        self.address('SP')
        self.write('A=M')  # A = M[SP]

    def inc_sp(self):
        self.address("SP")
        self.write('M=M+1')  # M[SP] = M[SP] + 1

    def dec_sp(self):
        self.address("SP")
        self.write('M=M-1')  # M[SP] = M[SP] - 1

    def write_arithmetic(self, command):

        if command not in unary:
            self.pop_D_from_stack()

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
            self.compare('JEQ')
        elif 'gt' == command:
            self.compare('JGT')
        elif 'lt' == command:
            self.compare('JLT')

        self.inc_sp()

    def write_init(self):
        self.copy_memory_to_address(256, "SP")  # M[SP] = 256
        self.write_call('Sys.init', 0)

    def write_if(self, location):
        self.pop_D_from_stack()
        self.address(location)
        self.write('D;JNE')  # if D == 0, jump to location else continue

    def write_goto(self, location):
        self.label(location)
        self.write('0;JMP')  # Jump to location

    def write_function(self, function_name, nb_locals):
        self.label(function_name)
        for i in range(int(nb_locals)):
            self.write("D=0")
            self.push_D_to_stack()

    def write_return(self):
        self.copy_memory_to_address(copy_to=get_address('frame'), copy_from=get_address('local'))
        self.address(5)
        self.write("A=D-A")
        self.write("D=M")
        self.copy_memory_to_address(copy_to=get_address('return'))
        self.pop_D_from_stack()
        self.D_to_ram(get_address('argument'))
        self.copy_memory_to_address(get_address('argument'), get_address('SP'))
        self.inc_sp()

        self.copy_memory_to_address(copy_to=get_address('temp'), copy_from=get_address('local'))

        for reg in ['local', 'argument', "this", "that"]:
            self.D_from_ram(get_address('temp'))
            self.write('D=D-1')
            self.copy_memory_to_address(copy_to=get_address(reg))

        self.write_goto(get_address('return'))  # goto RET

    def write_call(self, function_name, num_args):
        return_address = f"{function_name}.call.{self.call_index}"
        self.copy_memory_to_address(copy_to=get_address('frame'), copy_from=get_address('local'))

        for reg in ['local', 'argument', "this", "that"]:
            self.address(get_address(reg))
            self.write("D=M")
            self.push_D_to_stack()

        self.copy_memory_to_address(copy_from=get_address('SP'), copy_to=get_address('local'))

        self.address(int(num_args) + 5)
        self.write('D=D-A')
        self.address(get_address('argument'))
        self.write('M=D')

        self.write_goto(function_name)
        self.label(return_address)
        self.call_index += 1


    def label(self, label):
        self.write(f"({label})")

    def address(self, address):
        self.write(f"@{address}")

    def close(self):
        self.compiled_code.close()
