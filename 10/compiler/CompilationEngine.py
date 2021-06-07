from JackTokenizer import *
from SymbolTable import *


class CompilationEngine:

    def __init__(self, tokenizer, writer):
        self.writer = writer
        self.tokenizer = tokenizer
        if self.tokenizer.has_more_tokens():
            self.current_token = self.tokenizer.advance()
        self.compile_class()

    def write(self, string):
        self.writer.write(f'{string}')

    def start_tag(self, string):
        self.write(f"<{string}>\n")

    def end_tag(self, string):
        self.write(f"</{string}>\n")

    def process(self, token_str):
        if self.current_token.string == token_str:
            self.print_xml_token(self.current_token)
        else:
            print('error')
        if self.tokenizer.has_more_tokens():
            self.current_token = self.tokenizer.advance()

    def print_xml_token(self, token):
        # special chars of xml
        if token.string == '<':
            token.string = '&lt'
        elif token.string == '>':
            token.string = '&gt'
        elif token.string == '"':
            token.string = '&quot'
        elif token.string == '&':
            token.string = '&amp'

        if token.token_type == Types.SYMBOL:
            token.token_type = "symbol"
        elif token.token_type == Types.KEYWORD:
            token.token_type = "keyword"
        elif token.token_type == Types.IDENTIFIER:
            token.token_type = "identifier"
        elif token.token_type == Types.STRING_CONST:
            token.token_type = "stringConstant"
        elif token.token_type == Types.INT_CONST:
            token.token_type = "integerConstant"

        line = f"<{token.token_type}> {token.string} </{token.token_type}>"
        self.write(line + '\n')

    def print_and_advance(self, token):
        self.print_xml_token(token)
        if self.tokenizer.has_more_tokens():
            self.current_token = self.tokenizer.advance()

    def compile_class(self):
        self.start_tag('class')
        self.process('class')
        self.print_and_advance(self.current_token)
        self.process('{')
        while self.current_token.string == 'static' or self.current_token.string == 'field':
            self.compile_class_var_dec()
        while self.current_token.string == 'constructor' or self.current_token.string == 'function' or self.current_token.string == 'method':
            self.compile_subroutine()
        self.process('}')
        self.end_tag('class')

    def compile_class_var_dec(self):
        self.start_tag('classVarDec')
        if self.current_token.string == 'static':
            self.process('static')
        elif self.current_token.string == 'field':
            self.process('field')
        else:
            # end if there is not static or field
            return
            # print type
        self.print_and_advance(self.current_token)
        # print name
        self.print_and_advance(self.current_token)

        # handle comma variables
        while self.current_token.string == ',':
            self.process(',')
            self.print_and_advance(self.current_token)
        self.process(';')

        self.end_tag('classVarDec')

    def compile_subroutine(self):
        self.start_tag('subroutineDec')
        if self.current_token.string == 'constructor':
            self.process('constructor')
        elif self.current_token.string == 'function':
            self.process('function')
        elif self.current_token.string == 'method':
            self.process('method')

        # print type
        self.print_and_advance(self.current_token)
        # print name
        self.print_and_advance(self.current_token)
        self.process('(')
        self.compile_parameter_list()
        self.process(')')
        self.compile_subroutine_body()

        self.end_tag('subroutineDec')

    def compile_parameter_list(self):
        self.start_tag('parameterList')

        if (self.current_token.string == 'boolean' or
                self.current_token.string == 'char' or
                self.current_token.string == 'int' or
                self.current_token.token_type == Types.IDENTIFIER):

            # print type
            self.print_and_advance(self.current_token)
            # print name
            self.print_and_advance(self.current_token)

            # handle comma variables
            while self.current_token.string == ',':
                self.process(',')
                # print type
                self.print_and_advance(self.current_token)
                # print name
                self.print_and_advance(self.current_token)
        self.end_tag('parameterList')

    def compile_subroutine_body(self):
        self.start_tag('subroutineBody')
        self.process('{')
        while self.current_token.string == 'var':
            self.compile_var_dec()

        self.compile_statements()
        self.process('}')
        self.end_tag('subroutineBody')

    def compile_var_dec(self):
        self.start_tag('varDec')
        self.process('var')
        # print type
        self.print_and_advance(self.current_token)
        # print name
        self.print_and_advance(self.current_token)

        # handle comma variables
        while self.current_token.string == ',':
            self.process(',')
            self.print_and_advance(self.current_token)
        self.process(';')
        self.end_tag('varDec')

    def compile_statements(self):
        self.start_tag('statements')
        while True:
            if self.current_token.string == 'let':
                self.compile_let()
            elif self.current_token.string == 'if':
                self.compile_if()
            elif self.current_token.string == 'while':
                self.compile_while()
            elif self.current_token.string == 'do':
                self.compile_do()
            elif self.current_token.string == 'return':
                self.compile_return()
            else:
                break
        self.end_tag('statements')

    def compile_let(self):
        self.start_tag('letStatement')
        self.process('let')
        # print name
        self.print_and_advance(self.current_token)
        if self.current_token.string == '[':
            self.process('[')
            self.compile_expression()
            self.process(']')
        self.process('=')
        self.compile_expression()
        self.process(';')
        self.end_tag('letStatement')

    def compile_if(self):
        self.start_tag('ifStatement')
        self.process('if')
        self.process('(')
        self.compile_expression()
        self.process(')')
        self.process('{')
        self.compile_statements()
        self.process('}')
        if self.current_token.string == 'else':
            self.process('else')
            self.process('{')
            self.compile_statements()
            self.process('}')
        self.end_tag('ifStatement')

    def compile_while(self):
        self.start_tag('whileStatement')
        self.process('while')
        self.process('(')
        self.compile_expression()
        self.process(')')
        self.process('{')
        self.compile_statements()
        self.process('}')
        self.end_tag('whileStatement')

    def compile_do(self):
        self.start_tag('doStatement')
        self.process('do')
        self.compile_subroutine_call()
        self.process(';')
        self.end_tag('doStatement')

    def compile_subroutine_call(self):
        self.print_and_advance(self.current_token)
        if self.current_token.string == '.':
            self.process('.')
            self.print_and_advance(self.current_token)
        self.process('(')
        self.compile_expression_list()
        self.process(')')

    def compile_return(self):
        self.start_tag('returnStatement')
        self.process('return')
        if self.current_token.string != ';':
            self.compile_expression()
        self.process(';')
        self.end_tag('returnStatement')

    def compile_expression(self):
        self.start_tag('expression')

        while self.current_token not in [';', ')', ']', ',']:
            if self.current_token in OPERATORS:
                self.print_and_advance(self.current_token)
                self.tokenizer.advance()
            else:
                self.compile_term()

        self.end_tag('expression')

    def compile_term(self):
        self.start_tag('term')

        while self.current_token not in [';', ')', ']', ',']:
            if self.tokenizer.part_of_subroutine_call():
                self.compile_expression_list()
            elif self._starting_token_for('expression'):
                self.compile_expression()

        self.end_tag('term')

    def compile_expression_list(self):
        self.start_tag('expressionList')

        while self.current_token.token_type == Types.KEYWORD or self.current_token.token_type == Types.IDENTIFIER:
            self.compile_expression()
            if self.current_token.string != ',':
                break
            self.process(',')
        self.end_tag('expressionList')
