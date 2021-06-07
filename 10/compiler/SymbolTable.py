TERMINAL_TOKEN_TYPES = ["STRING_CONST", "INT_CONST", "IDENTIFIER", "SYMBOL"]
TERMINAL_KEYWORDS = ["boolean", "class", "void", "int"]
CLASS_VAR_DEC_TOKENS = ["static", "field"]
SUBROUTINE_TOKENS = ["function", "method", "constructor"]
STATEMENT_TOKENS = ['do', 'let', 'while', 'return', 'if']
STARTING_TOKENS = {
    'var_dec': ['var'],
    'parameter_list': ['('],
    'subroutine_body': ['{'],
    'expression_list': ['('],
    'expression': ['=', '[', '(']
}
TERMINATING_TOKENS = {
    'class': ['}'],
    'class_var_dec': [';'],
    'subroutine': ['}'],
    'parameter_list': [')'],
    'expression_list': [')'],
    'statements': ['}'],
    'do': [';'],
    'let': [';'],
    'while': ['}'],
    'if': ['}'],
    'var_dec': [';'],
    'return': [';'],
    'expression': [';', ')', ']', ',']
}
OPERATORS = [
    '+',
    '-',
    '*',
    '/',
    '&amp;',
    '|',
    '&lt;',
    '&gt;',
    '='
]
UNARY_OPERATORS = ['-', '~']