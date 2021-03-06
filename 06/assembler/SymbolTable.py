
class SymbolTable:

    def __init__(self, load_predefined=True):
        self.table = {}
        self.data_address = 0
        self.program_address = 0
        if load_predefined:
            self.add_predefined_symbols()

    def add_predefined_symbols(self):
        entries = dict(
            SP=0,
            LCL=1,
            ARG=2,
            THIS=3,
            THAT=4,
            R0=0,
            R1=1,
            R2=2,
            R3=3,
            R4=4,
            R5=5,
            R6=6,
            R7=7,
            R8=8,
            R9=9,
            R10=10,
            R11=11,
            R12=12,
            R13=13,
            R14=14,
            R15=15,
            SCREEN=16384,
            KBD=24576
        )
        self.data_address = 16
        self.table.update(entries)

    def add_entry(self, symbol, address) -> None:
        self.table[symbol] = address

    def contains(self, symbol) -> bool:
        return symbol in self.table

    def get_address(self, symbol) -> int:
        return self.table[symbol]

    def get_program_address(self):
        return self.program_address

    def get_data_address(self):
        return self.data_address

    def increment_data_address(self):
        self.data_address += 1

    def increment_address(self):
        self.program_address += 1
