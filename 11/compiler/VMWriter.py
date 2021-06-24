class VMWriter():

    __arithmetic_symbols = {
        '+': 'add',
        '-': 'sub',
        '>': 'gt',
        '<': 'lt',
        '=': 'eq',
        '&': 'and',
        '|': 'or'
    }

    __unary_symbols = {
        '-': 'neg',
        '~': 'not'
    }

    def __init__(self, writer):
        self.writer = writer

    def write(self, string):
        self.writer.write(f'{string}\n')

    def write_push(self, segment, index):
        self.write(f"push {segment} {index}")

    def write_pop(self, segment, index):
        self.write(f"pop {segment} {index}")

    def write_arithmetic(self, command):
        self.write(VMWriter.__arithmetic_symbols.get(command, command))

    def write_unary(self, command):
        self.write(VMWriter.__unary_symbols.get(command, command))

    def write_label(self, label):
        self.write(f"label {label}")

    def write_goto(self, label):
        self.write(f"goto {label}")

    def write_if_goto(self, label):
        self.write(f"if-goto {label}")

    def write_call(self, name, nb_vars):
        self.write(f"call {name} {nb_vars}")

    def write_function(self, name, nb_locals):
        self.write(f"function {name} {nb_locals}")

    def write_return(self):
        self.write("return")

    def close(self):
        self.writer.close()
