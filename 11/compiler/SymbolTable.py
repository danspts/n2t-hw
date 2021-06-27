class IdentifierCategory:
    IDENTIFIER_VAR = 1
    IDENTIFIER_ARGUMENT = 2
    IDENTIFIER_STATIC = 3
    IDENTIFIER_FIELD = 4
    IDENTIFIER_CLASS = 5
    IDENTIFIER_SUBROUTINE = 6


class SymbolTable():

    def __init__(self):
        self.symbols = {}
        self.running_index_var = 0
        self.running_index_argument = 0
        self.running_index_static = 0
        self.running_index_field = 0

    def define(self, name, identifier_category):
        index_value = -1
        if identifier_category == IdentifierCategory.IDENTIFIER_VAR:
            index_value = self.running_index_var
            self.running_index_var += 1
        elif identifier_category == IdentifierCategory.IDENTIFIER_ARGUMENT:
            index_value = self.running_index_argument
            self.running_index_argument += 1
        elif identifier_category == IdentifierCategory.IDENTIFIER_STATIC:
            index_value = self.running_index_static
            self.running_index_static += 1
        elif identifier_category == IdentifierCategory.IDENTIFIER_FIELD:
            index_value = self.running_index_field
            self.running_index_field += 1

        if index_value == -1:
            self.symbols[name] = dict(
                identifier_category=identifier_category,
            )
        else:
            self.symbols[name] = dict(
                identifier_category=identifier_category,
                index=index_value
            )
        return index_value

    def var_count(self, kind):
        return sum(1 if symbol['kind'] == kind else 0 for symbol in self.symbols)

    def kind_of(self, name):
        return self.symbols[name]["kind"]

    def type_of(self, name):
        return self.symbols[name]["type"]

    def index_of(self, name):
        return self.symbols[name]["index"]
