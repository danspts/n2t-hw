from JackTokenizer import VariableKind


class SymbolTable:
    def __init__(self):
        self.class_symbol_table = SymbolTableSt()
        self.subroutine_symbol_table = SymbolTableSt()
        self.var_index_value = 0
        self.argument_index_value = 0
        self.static_index_value = 0
        self.field_index_value = 0

    def get_var(self, name):
        if self.subroutine_symbol_table.is_in_table(name):
            return self.subroutine_symbol_table.symbols[name]
        elif self.class_symbol_table.is_in_table(name):
            return self.class_symbol_table.symbols[name]
        else:
            return None

    def reset_sub(self):
        self.subroutine_symbol_table = SymbolTableSt()
        self.var_index_value = 0
        self.argument_index_value = 0
        self.static_index_value = 0
        self.field_index_value = 0

    def define(self, name, symbol_type, kind):
        if kind == VariableKind.LOCAL:
            self.subroutine_symbol_table.symbols[name] = dict(
                type=symbol_type,
                kind=kind,
                index=self.var_index_value
            )
            self.var_index_value += 1
            return self.var_index_value - 1
        elif kind == VariableKind.ARGUMENT:
            self.subroutine_symbol_table.symbols[name] = dict(
                type=symbol_type,
                kind=kind,
                index=self.argument_index_value
            )
            self.argument_index_value += 1
            return self.argument_index_value - 1
        elif kind == VariableKind.FIELD:
            self.class_symbol_table.symbols[name] = dict(
                type=symbol_type,
                kind=kind,
                index=self.field_index_value
            )
            self.field_index_value += 1
            return self.field_index_value - 1
        elif kind == VariableKind.STATIC:
            self.class_symbol_table.symbols[name] = dict(
                type=symbol_type,
                kind=kind,
                index=self.static_index_value
            )
            self.static_index_value += 1
            return self.static_index_value - 1


class SymbolTableSt:

    def __init__(self):
        self.symbols = {}

    def var_count(self, kind):
        return sum(1 if symbol['kind'] == kind else 0 for symbol in self.symbols)

    def kind_of(self, name):
        return self.symbols[name]["kind"]

    def type_of(self, name):
        return self.symbols[name]["type"]

    def index_of(self, name):
        return self.symbols[name]["index"]

    def is_in_table(self, name):
        return name in self.symbols.keys()
