


class SymbolTable():

    def __init__(self):
        self.symbols = {}
        self.index_value = 0

    def define(self, name, symbol_type, kind):
        self.symbols[name] = dict(
            type=symbol_type,
            kind=kind,
            index=self.index_value
        )
        self.index_value += 1

    def var_count(self, kind):
        return sum(1 if symbol['kind'] == kind else 0 for symbol in self.symbols)

    def kind_of(self, name):
        return self.symbols[name]["kind"]

    def type_of(self, name):
        return self.symbols[name]["type"]

    def index_of(self, name):
        return self.symbols[name]["index"]
