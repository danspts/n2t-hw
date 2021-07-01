from VMWriter import VMWriter
from JackTokenizer import *
from SymbolTable import SymbolTable


class FunctionTracker:
    def __init__(self):
        self.subroutine = ""
        self.name = ""
        self.num_of_vars = ""


class VariableTracker:
    def __init__(self):
        self.running_index = 0
        self.type = None
        self.kind = None
        self.variable_scope = None
        self.variables = []


class CompilationEngine:

    def __init__(self, tokenizer, writer):
        self.writer = VMWriter(writer)
        self.vm_writer = VMWriter(writer)
        self._class = ""
        self.function_tracker = FunctionTracker()
        self.symbol_table = SymbolTable()
        self.variable_tracker = VariableTracker()
        self.tokenizer = tokenizer
        self.label_index = 0
        if self.tokenizer.has_more_tokens():
            self.current_token = self.tokenizer.advance()
        self.compile_class()

    def write(self, string):
        # print(string)
        self.writer.write(f'{string}')

    def start_token(self, string):
        pass
        # self.write(f"<{string}>\n")

    def end_token(self, string):
        pass
        # self.write(f"</{string}>\n")

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

        if token.is_variable:
            if token.variable_info.running_index != -1:
                line = f"<{token.token_type}>name: {token.string} category: {token.variable_info.kind} type: {token.variable_info.type} running index = {token.variable_info.running_index}</{token.token_type}>"
            else:
                line = f"<{token.token_type}>name: {token.string} category: {token.variable_info.kind} type: {token.variable_info.type}</{token.token_type}>"
        else:
            line = f"<{token.token_type}> {token.string} </{token.token_type}>"

        # self.write(line + '\n')

    def advance(self, token):
        # self.print_xml_token(token)

        if self.tokenizer.has_more_tokens():
            self.current_token = self.tokenizer.advance()

    def compile_class(self):
        self.start_token('class')
        self.process('class')
        self._class = self.current_token.string
        self.advance(self.current_token)
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
            self.variable_tracker.kind = VariableKind.STATIC
        elif self.current_token.string == 'field':
            self.process('field')
            self.variable_tracker.kind = VariableKind.FIELD
        else:
            # end if there is not static or field
            return
        # print type
        self.variable_tracker.type = self.current_token.string
        self.advance(self.current_token)

        # print name
        self.current_token.is_variable = True
        self.current_token.variable_info.type = self.variable_tracker.type
        self.current_token.variable_info.kind = self.variable_tracker.kind
        self.current_token.variable_info.running_index = self.symbol_table.define(self.current_token.string,
                                                                                  self.variable_tracker.type,
                                                                                  self.variable_tracker.kind)
        self.advance(self.current_token)

        # handle comma variables
        while self.current_token.string == ',':
            self.process(',')
            self.current_token.is_variable = True
            self.current_token.variable_info.type = self.variable_tracker.type
            self.current_token.variable_info.kind = self.variable_tracker.kind
            self.current_token.variable_info.running_index = self.symbol_table.define(self.current_token.string,
                                                                                      self.variable_tracker.type,
                                                                                      self.variable_tracker.kind)
            self.advance(self.current_token)

        self.process(';')

        self.end_token('classVarDec')

    def compile_subroutine(self):
        self.start_token('subroutineDec')
        self.function_tracker.subroutine = self.current_token.string
        if self.function_tracker.subroutine == 'constructor':
            self.process('constructor')
        elif self.function_tracker.subroutine == 'function':
            self.process('function')
            self.symbol_table.reset_sub()
        elif self.function_tracker.subroutine == 'method':
            self.process('method')
            self.symbol_table.reset_sub()


        # print type
        self.advance(self.current_token)
        # print name
        name = self.current_token.string
        self.function_tracker.name = name
        self.advance(self.current_token)
        self.process('(')
        num_of_params = self.compile_parameter_list()
        self.process(')')
        self.function_tracker.num_of_vars = num_of_params
        self.compile_subroutine_body(name)

        self.end_token('subroutineDec')

    def compile_parameter_list(self):
        self.start_token('parameterList')
        numb_of_param = 0

        if (self.current_token.string == 'boolean' or
                self.current_token.string == 'char' or
                self.current_token.string == 'int' or
                self.current_token.token_type == Types.IDENTIFIER):

            self.variable_tracker.kind = VariableKind.ARGUMENT
            # print type
            self.advance(self.current_token)
            self.variable_tracker.type = self.current_token.string
            # print name
            self.current_token.is_variable = True
            self.current_token.variable_info.type = self.variable_tracker.type
            self.current_token.variable_info.kind = self.variable_tracker.kind
            self.current_token.variable_info.running_index = self.symbol_table.define(self.current_token.string,
                                                                                      self.variable_tracker.type,
                                                                                      self.variable_tracker.kind)

            self.advance(self.current_token)
            numb_of_param += 1

            # handle comma variables
            while self.current_token.string == ',':
                self.process(',')
                # print type
                self.variable_tracker.type = self.current_token.string
                self.advance(self.current_token)
                # print name
                self.current_token.is_variable = True
                self.current_token.variable_info.type = self.variable_tracker.type
                self.current_token.variable_info.kind = self.variable_tracker.kind
                self.current_token.variable_info.running_index = self.symbol_table.define(self.current_token.string,
                                                                                          self.variable_tracker.type,
                                                                                          self.variable_tracker.kind)

                self.advance(self.current_token)
                numb_of_param += 1

        self.end_token('parameterList')
        return numb_of_param

    def compile_subroutine_body(self, subroutine_name):
        self.start_token('subroutineBody')
        self.process('{')
        nb_var = 0
        while self.current_token.string == 'var':
            nb_var += self.compile_var_dec()

        if self.function_tracker.subroutine == 'constructor':
            self.writer.write_function(f"{self._class}.{self.function_tracker.name}", nb_var)
            self.writer.write(f"push constant { self.symbol_table.get_num_class()}")
            self.writer.write(f"call Memory.alloc 1")
            self.writer.write(f"pop pointer 0")
        elif self.function_tracker.subroutine == 'function':
            self.writer.write_function(f"{self._class}.{self.function_tracker.name}", nb_var)
        elif self.function_tracker.subroutine == 'method':
            self.writer.write_function(f"{self._class}.{self.function_tracker.name}", nb_var)
            self.vm_writer.write('push argument 0\npop pointer 0')


        self.compile_statements()
        self.process('}')
        self.end_token('subroutineBody')

    def compile_var_dec(self):
        self.start_token('varDec')
        self.process('var')
        self.variable_tracker.kind = VariableKind.LOCAL
        # print type
        self.variable_tracker.type = self.current_token.string
        self.advance(self.current_token)
        # print name
        # print(self.current_token.__dict__)
        self.current_token.is_variable = True
        self.current_token.variable_info.type = self.variable_tracker.type
        self.current_token.variable_info.kind = self.variable_tracker.kind
        self.current_token.variable_info.running_index = self.symbol_table.define(self.current_token.string,
                                                                                  self.variable_tracker.type,
                                                                                  self.variable_tracker.kind)

        self.advance(self.current_token)
        nb_var = 1
        # handle comma variables
        while self.current_token.string == ',':
            nb_var += 1
            self.process(',')
            self.current_token.is_variable = True
            self.current_token.variable_info.type = self.variable_tracker.type
            self.current_token.variable_info.kind = self.variable_tracker.kind
            self.current_token.variable_info.running_index = self.symbol_table.define(self.current_token.string,
                                                                                      self.variable_tracker.type,
                                                                                      self.variable_tracker.kind)

            self.advance(self.current_token)
        self.process(';')
        self.end_token('varDec')
        return nb_var

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
        self.current_token.is_variable = True
        self.current_token.variable_info.type = self.symbol_table.get_var(self.current_token.string)['type']
        self.current_token.variable_info.kind = self.symbol_table.get_var(self.current_token.string)['kind']
        self.current_token.variable_info.running_index = self.symbol_table.get_var(self.current_token.string)['index']
        token = self.current_token
        self.advance(self.current_token)
        if self.current_token.string == '[':
            self.process('[')
            self.compile_expression()
            self.process(']')
        self.process('=')
        self.compile_expression()
        self.process(';')
        self.end_token('letStatement')
        self.vm_writer.write_pop_var(token)

    def compile_if(self):
        label_1 = f'IF_TRUE{self.label_index}'
        self.label_index += 1
        label_2 = f'IF_FALSE{self.label_index}'
        self.label_index += 1
        self.start_token('ifStatement')
        self.process('if')
        self.process('(')
        self.compile_expression()
        self.process(')')
        self.vm_writer.write('not')
        self.vm_writer.write_if_goto(label_1)
        self.process('{')
        self.compile_statements()
        self.process('}')
        self.vm_writer.write_goto(label_2)
        self.vm_writer.write_label(label_1)
        if self.current_token.string == 'else':
            self.process('else')
            self.process('{')
            self.compile_statements()
            self.process('}')
        self.end_token('ifStatement')
        self.vm_writer.write_label(label_2)

    def compile_while(self):
        label_1 = f'WHILE_EXP{self.label_index}'
        self.label_index += 1
        label_2 = f'WHILE_END{self.label_index}'
        self.label_index += 1
        self.vm_writer.write_label(label_1)
        self.start_token('whileStatement')
        self.process('while')
        self.process('(')
        self.compile_expression()
        self.process(')')
        self.vm_writer.write('not')
        self.vm_writer.write_if_goto(label_2)

        self.process('{')
        self.compile_statements()
        self.process('}')
        self.vm_writer.write_goto(label_1)
        self.vm_writer.write_label(label_2)
        self.end_token('whileStatement')

    def compile_do(self):
        self.start_token('doStatement')
        self.process('do')
        self.compile_subroutine_call()
        self.process(';')
        self.end_token('doStatement')
        self.vm_writer.write('pop temp 0')

    def compile_subroutine_call(self):
        have_point = False
        num_of_exp = 0
        var = self.symbol_table.get_var(self.current_token.string)
        if var is not None:
            self.current_token.is_variable = True
            self.current_token.variable_info.type = self.symbol_table.get_var(self.current_token.string)['type']
            self.current_token.variable_info.kind = self.symbol_table.get_var(self.current_token.string)['kind']
            self.current_token.variable_info.running_index = self.symbol_table.get_var(self.current_token.string)[
                'index']
            self.vm_writer.write_push_var(self.current_token)
            num_of_exp += 1
            self.variable_tracker.type = self.current_token.token_type
            sub_name = self.current_token.variable_info.type
        else:
            sub_name = self.current_token.string
        self.advance(self.current_token)
        if self.current_token.string == '.':
            have_point = True
            self.process('.')
            sub_name += '.' + self.current_token.string
            self.advance(self.current_token)
        else:
            sub_name = self._class + '.' + sub_name
        self.process('(')
        num_of_exp += self.compile_expression_list()
        self.process(')')
        if not have_point and var is None:
            # method call in object
            self.vm_writer.write('push pointer 0')
            num_of_exp += 1
        self.vm_writer.write_call(sub_name, num_of_exp)


    def compile_return(self):
        self.start_token('returnStatement')
        self.process('return')
        if self.current_token.string != ';':
            self.compile_expression()
        else:
            self.vm_writer.write_push_const('0')
        self.process(';')
        self.end_token('returnStatement')
        self.vm_writer.write_return()

    def compile_expression(self):
        self.start_token('expression')
        self.compile_term()

        while self.current_token.string in list('+-*/&|<>='):
            op = self.current_token.string
            self.advance(self.current_token)
            self.compile_term()
            self.vm_writer.write_arithmetic(op)

        self.end_token('expression')

    def compile_term(self):
        self.start_token('term')

        if self.current_token.string == '(':
            self.process('(')
            self.compile_expression()
            self.process(')')
        else:
            if self.current_token.string == '-' or self.current_token.string == '~':
                op = self.current_token.string
                self.advance(self.current_token)
                self.compile_term()
                self.vm_writer.write_unary(op)
            else:
                function_name = self.current_token.string
                var = self.symbol_table.get_var(self.current_token.string)
                if var is not None:
                    self.current_token.is_variable = True
                    self.current_token.variable_info.type = self.symbol_table.get_var(self.current_token.string)['type']
                    self.current_token.variable_info.kind = self.symbol_table.get_var(self.current_token.string)['kind']
                    self.current_token.variable_info.running_index = \
                        self.symbol_table.get_var(self.current_token.string)[
                            'index']
                    self.vm_writer.write_push_var(self.current_token)
                    self.advance(self.current_token)
                else:
                    if not self.current_token.string.isnumeric() and self.current_token.token_type != Types.STRING_CONST and self.current_token.token_type != Types.KEYWORD:
                        self.compile_subroutine_call()
                    else:
                        if self.current_token.string == 'true':
                            self.vm_writer.write_push_const('0')
                            self.vm_writer.write_unary('~')
                        elif self.current_token.string == 'false' or self.current_token.string == 'null':
                            self.vm_writer.write_push_const('0')
                        elif self.current_token.string == 'this':
                            self.vm_writer.write('push pointer 0')
                        else:
                            if self.current_token.token_type == Types.STRING_CONST:
                                self.vm_writer.write_push_const(len(self.current_token.string))
                                self.vm_writer.write('call String.new 1')
                                for i in self.current_token.string:
                                    self.vm_writer.write_push_const(ord(i))
                                    self.vm_writer.write('call String.appendChar 2')
                            else:
                                self.vm_writer.write_push_const(self.current_token.string)
                        self.advance(self.current_token)

                if self.current_token.string == '[':
                    self.process('[')
                    self.compile_expression()
                    self.process(']')
                elif self.current_token.string == '(':
                    self.process('(')
                    num_of_vars = self.compile_expression_list()
                    self.process(')')
                    self.vm_writer.write_call(function_name, num_of_vars)
                elif self.current_token.string == '.':
                    self.process('.')
                    self.advance(self.current_token)
                    self.process('(')
                    num_of_vars = self.compile_expression_list()
                    self.process(')')
                    self.vm_writer.write_call(function_name, num_of_vars + 1)

        self.end_token('term')

    def compile_expression_list(self):
        self.start_token('expressionList')
        num_of_exp = 0

        while self.current_token.string != ')':
            num_of_exp += 1
            self.compile_expression()
            if self.current_token.string != ',':
                break
            self.process(',')
        self.end_token('expressionList')
        return num_of_exp
