from JackTokenizer import *


class CompilationEngine:

    def __init__(self, tokenizer, writer):
        self.writer = writer
        self.tokenizer = tokenizer
        self.current_token = self.tokenizer.advance()
        self.compile_class()

    def process(self, token_str):
        if self.current_token.string == token_str:
            self.print_xml_token(self.current_token)
        else:
            print('error')
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
        self.writer.write(line + '\n')

    def print_and_advance(self, token):
        self.print_xml_token(token)
        self.current_token = self.tokenizer.advance()

    def compile_class(self):
        self.writer.write('<class>\n')
        self.process('class')
        self.print_and_advance(self.current_token)
        self.process('{')
        while self.current_token.string == 'static' or self.current_token.string == 'field':
            self.compile_class_var_dec()
        while self.current_token.string == 'constructor' or self.current_token.string == 'function' or self.current_token.string == 'method':
            self.compile_subroutine()
        self.process('}')
        self.writer.write('</class>\n')

    def compile_class_var_dec(self):
        self.writer.write('<classVarDec>\n')
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

        self.writer.write('</classVarDec>\n')

    def compile_subroutine(self):
        if self.current_token.string == 'constructor':
            self.writer.write('<subroutineDec>\n')
            self.process('constructor')
        elif self.current_token.string == 'function':
            self.writer.write('<subroutineDec>\n')
            self.process('function')
        elif self.current_token.string == 'method':
            self.writer.write('<subroutineDec>\n')
            self.process('method')
        else:
            # end if there is not static or field
            return

        # print type
        self.print_and_advance(self.current_token)
        # print name
        self.print_and_advance(self.current_token)
        self.process('(')
        self.compile_parameter_list()
        self.process(')')
        self.compile_subroutine_body()

        self.compile_subroutine()

        self.writer.write('</subroutineDec>\n')

    def compile_parameter_list(self):
        if not (
                self.current_token.string == 'boolean' or
                self.current_token.string == 'char' or
                self.current_token.string == 'int' or
                self.current_token.token_type == Types.IDENTIFIER):
            return
        self.writer.write('<parameterList>\n')

        # print type
        self.print_and_advance(self.current_token)
        # print name
        self.print_and_advance(self.current_token)

        # handle comma variables
        while self.current_token.string == ',':
            self.process(',')
            self.print_and_advance(self.current_token)
        self.process(';')
        self.writer.write('</parameterList>\n')

    def compile_subroutine_body(self):
        self.writer.write('<subroutineBody>\n')
        self.process('{')
        self.compile_var_dec()
        self.compile_statements()
        self.process('}')
        self.writer.write('</subroutineBody>\n')


    def compile_var_dec(self):
        self.writer.write('<varDec>\n')
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
        self.writer.write('</varDec>\n')

    def compile_statements(self):
        self.writer.write('<statements>\n')
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
            return
        self.compile_statements()
        self.writer.write('</statements>\n')


    def compile_let(self):
        self.writer.write('<letStatement>\n')
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
        self.writer.write('</letStatement>\n')

    def compile_if(self):
        self.writer.write('<ifStatement>\n')
        self.process('if')
        self.process(')')
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
        self.writer.write('</ifStatement>\n')

    def compile_while(self):
        self.writer.write('<whileStatement>\n')
        self.process('while')
        self.process('(')
        self.compile_expression()
        self.process(')')
        self.process('{')
        self.compile_statements()
        self.process('}')
        self.writer.write('</whileStatement>\n')

    def compile_do(self):
        self.writer.write('<doStatement>\n')
        self.process('do')
        self.compile_subroutine_call()
        self.process(';')
        self.writer.write('</doStatement>\n')

    def compile_subroutine_call(self):
        self.print_and_advance(self.current_token)
        if self.current_token.string == '.':
            self.process('.')
            self.print_and_advance(self.current_token)
        self.process('(')
        self.compile_expression_list()
        self.process(')')

    def compile_return(self):
        self.writer.write('<returnStatement>\n')
        self.process('return')
        self.compile_expression()
        self.process(';')
        self.writer.write('</returnStatement>\n')

    def compile_expression(self):
        self.writer.write('<expression>\n')
        self.print_and_advance(self.current_token)
        # self.compile_term()
        #
        # while self.current_token.string in list('+-*/&|<>='):
        #     self.print_and_advance(self.current_token)
        #     self.compile_term()
        self.writer.write('</expression>\n')

    def compile_term(self):
        self.writer.write('<term>\n')

        # if self.current_token.token_type == Types.INT_CONST or self.current_token.token_type == Types.STRING_CONST or \
        #     self.current_token.string == 'true' or \
        #     self.current_token.string == 'false' or \
        #     self.current_token.string == 'null' or \
        #     self.current_token.string == 'this' or:
        #     pass
        self.writer.write('</term>\n')

    def compile_expression_list(self):
        self.writer.write('<expressionList>\n')
        self.writer.write('</expressionList>\n')
