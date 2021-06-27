from JackTokenizer import Types

class SymbolTable:
    def __init__(self):
        self.var_index = 0
        self.argument_index = 0
        self.static_index = 0
        self.field_index = 0
        self.table = dict()

    def in_table(self, token):
        return token.string in self.table.keys()

    def add_to_table(self, token):

        if token.token_type == Types.IDENTIFIER_VAR:
            self.table[token.string] = dict(string=token.string, token_type=token.token_type, index=self.var_index)
            self.var_index += 1
        elif token.token_type == Types.IDENTIFIER_ARGUMENT:
            self.table[token.string] = dict(string=token.string, token_type=token.token_type, index=self.argument_index)
            self.argument_index += 1
        elif token.token_type == Types.IDENTIFIER_STATIC:
            self.table[token.string] = dict(string=token.string, token_type=token.token_type, index=self.static_index)
            self.static_index += 1
        elif token.token_type == Types.IDENTIFIER_FIELD:
            self.table[token.string] = dict(string=token.string, token_type=token.token_type, index=self.field_index)
            self.field_index += 1
        elif token.token_type == Types.IDENTIFIER_CLASS:
            self.table[token.string] = dict(string=token.string, token_type=token.token_type, index=0)
        else:
            self.table[token.string] = dict(string=token.string, token_type=token.token_type, index=0)

    def get(self, token):
        return self.table[token.string]
