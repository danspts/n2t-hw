from JackTokenizer import *


class CompilationEngine:

    def __init__(self, tokenizer, writer):
        self.writer = writer
        self.tokenizer = tokenizer
        if self.tokenizer.has_more_tokens():
            self.current_token = self.tokenizer.advance()
        self.compile_class()

    def write(self, string):
        self.writer.write(f'{string}')

    def start_token(self, string):
        self.write(f"<{string}>\n")

    def end_token(self, string):
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
            token.string = '&lt;'
        elif token.string == '>':
            token.string = '&gt;'
        elif token.string == '"':
            token.string = '&quot;'
        elif token.string == '&':
            token.string = '&amp;'

        line = f"<{token.token_type}> {token.string} </{token.token_type}>"
        self.write(line + '\n')

    def print_and_advance(self, token):
        self.print_xml_token(token)
        if self.tokenizer.has_more_tokens():
            self.current_token = self.tokenizer.advance()

    def compile_class(self):
        self.start_token('class')
        self.process('class')
        self.print_and_advance(self.current_token)
        self.process('{')
        while self.current_token.string == 'static' or self.current_token.string == 'field':
            self.compile_class_var_dec()
        while self.current_token.string == 'constructor' or self.current_token.string == 'function' or self.current_token.string == 'method':
            self.compile_subroutine()
        self.process('}')
        self.end_token('class')

    def compile_class_var_dec(self):
        self.start_token('classVarDec')
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

        self.end_token('classVarDec')

    def compile_subroutine(self):
        self.start_token('subroutineDec')
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

        self.end_token('subroutineDec')

    def compile_parameter_list(self):
        self.start_token('parameterList')

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
        self.end_token('parameterList')

    def compile_subroutine_body(self):
        self.start_token('subroutineBody')
        self.process('{')
        while self.current_token.string == 'var':
            self.compile_var_dec()

        self.compile_statements()
        self.process('}')
        self.end_token('subroutineBody')


    def compile_var_dec(self):
        self.start_token('varDec')
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
        self.end_token('varDec')

    def compile_statements(self):
        self.start_token('statements')
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
        self.end_token('statements')


    def compile_let(self):
        self.start_token('letStatement')
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
        self.end_token('letStatement')

    def compile_if(self):
        self.start_token('ifStatement')
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
        self.end_token('ifStatement')

    def compile_while(self):
        self.start_token('whileStatement')
        self.process('while')
        self.process('(')
        self.compile_expression()
        self.process(')')
        self.process('{')
        self.compile_statements()
        self.process('}')
        self.end_token('whileStatement')

    def compile_do(self):
        self.start_token('doStatement')
        self.process('do')
        self.compile_subroutine_call()
        self.process(';')
        self.end_token('doStatement')

    def compile_subroutine_call(self):
        self.print_and_advance(self.current_token)
        if self.current_token.string == '.':
            self.process('.')
            self.print_and_advance(self.current_token)
        self.process('(')
        self.compile_expression_list()
        self.process(')')

    def compile_return(self):
        self.start_token('returnStatement')
        self.process('return')
        if self.current_token.string != ';':
            self.compile_expression()
        self.process(';')
        self.end_token('returnStatement')

    def compile_expression(self):
        self.start_token('expression')
        self.compile_term()

        while self.current_token.string in list('+-*/&|<>='):
            self.print_and_advance(self.current_token)
            self.compile_term()
        self.end_token('expression')

    def compile_term(self):
        self.start_token('term')

        if self.current_token.string == '(':
            self.process('(')
            self.compile_expression()
            self.process(')')
        else:
            if self.current_token.string == '-' or self.current_token.string == '~':
                self.print_and_advance(self.current_token)
                self.compile_term()
            else:
                self.print_and_advance(self.current_token)
                if self.current_token.string == '[':
                    self.process('[')
                    self.compile_expression()
                    self.process(']')
                elif self.current_token.string == '(':
                    self.process('(')
                    self.compile_expression_list()
                    self.process(')')
                elif self.current_token.string == '.':
                    self.process('.')
                    self.print_and_advance(self.current_token)
                    self.process('(')
                    self.compile_expression_list()
                    self.process(')')

        self.end_token('term')

    def compile_expression_list(self):
        self.start_token('expressionList')

        while self.current_token.string != ')':
            self.compile_expression()
            if self.current_token.string != ',':
                break
            self.process(',')
        self.end_token('expressionList')
