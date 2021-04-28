
class SymbolTable:

    def __init__(self):
        self.table = {}

    def add_entry(self, symbol, address) -> None:
        self.table.setdefault(symbol, address)

    def contains(self, symbol) -> bool:
        return symbol in self.table
    
    def get_address(self, symbol) -> int:
        return self.table.getdefault(symbol, -1)