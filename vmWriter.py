from xml.etree import ElementTree

import TokensMapping
from TokensMapping import LabelTypes
from symbolTable import SymbolTable

kind_to_segment = {'static': 'static',
                   'field': 'this',
                   'arg': 'argument',
                   'var': 'local'}

CLASS = 'class'
SUBROUTINE_DEC = "subroutineDec"
PARAMETER_LIST = "parameterList"
SUBROUTINE_BODY = "subroutineBody"
STATEMENTS = "statements"
LET_STATEMENT = "letStatement"
IF_STATEMENT = "ifStatement"
WHILES_TATEMENT = "whileStatement"
DO_STATEMENT = "doStatement"
RETURN_STATEMENT = "returnStatement"
EXPRESSION = "expression"
TERM = "term"
EXPRESSION_LIST = "expressionList"
SYMBOL = "symbol"
KEYWORD = "keyword"
IDENTIFIER = "identifier"


class vmWriter:
    def __init__(self, output_file):
        self.output_file = output_file
        self.label_count = 0
        self.symbol_table = SymbolTable()

    def compile_vars(self, element):
        kind, type = list(element)[:2]
        for name in list(element)[2:]:
            if name == ",":
                continue
            if name == ";":
                break
            self.symbol_table.define(name.text, type.text, kind.text)

    def write_tree(self, element: ElementTree.Element, parent=None):
        if element.tag in (LabelTypes.CLASS_VAR_DEC, LabelTypes.VAR_DEC):
            self.compile_vars(element)
        if element.tag == LabelTypes.STRING_CONSTANT:
            string = element.text
            self.write_push("constant", len(string))
            self.write_call("String.new", 1)
            for i in string:
                self.write_push("constant", ord(i))
                self.write_call("String.appendChar", 2)
        if element.tag == LabelTypes.INTEGER_CONSTANT:
            self.write_push("constant", element.text)
        if element.tag == LabelTypes.TERM:
            self.compile_term(element)
        for child in element:
            self.write_tree(child, parent)

    def write_if(self, label):
        self.output_file.write('not\n')  # Negate to jump if the conditions doesn't hold
        self.output_file.write('if-goto {}\n'.format(label))

    def write_goto(self, label):
        self.output_file.write('goto {}\n'.format(label))

    def write_label(self, label):
        self.output_file.write('label {}\n'.format(label))

    def write_function(self, jack_subroutine):
        class_name = jack_subroutine.jack_class.name
        name = jack_subroutine.name
        local_vars = jack_subroutine.var_symbols

        self.output_file.write('function {}.{} {}\n'.format(class_name, name, local_vars))

    def write_return(self):
        self.output_file.write('return\n')

    def write_call(self, func_name, arg_count):
        self.output_file.write('call {} {}\n'.format(
            func_name, arg_count
        ))

    def write_pop_symbol(self, jack_symbol):
        kind = jack_symbol.kind
        offset = jack_symbol.id  # the offset in the segment

        segment = kind_to_segment[kind]
        self.write_pop(segment, offset)

    def write_push_symbol(self, jack_symbol):
        kind = jack_symbol.kind
        offset = jack_symbol.id  # the offset in the segment

        segment = kind_to_segment[kind]
        self.write_push(segment, offset)

    def write_pop(self, segment, offset):
        self.output_file.write('pop {0} {1}\n'.format(segment, offset))

    def write_push(self, segment, offset):
        self.output_file.write('push {0} {1}\n'.format(segment, offset))

    def write(self, vm_line):
        self.output_file.write('{}\n'.format(vm_line))

    def write_constant(self, n):
        self.write_push('constant', n)

    def write_string(self, s):
        s = s[1:-1]
        self.write_constant(len(s))
        self.write_call('String', 'new', 1)
        for c in s:
            self.write_constant(ord(c))
            self.write_call('String', 'appendChar', 2)

    def compile_term(self, element):
        children = list(element)
        if len(children) == 1:
            child = children[0]
            if child.tag == TokensMapping.TokenTypes.INT:
                self.write_push("constant", element.text)

            elif child.tag == TokensMapping.TokenTypes.STRING:
                self.handle_str()

            elif element.tag == TokensMapping.TokenTypes.IDENTIFIER:
                value = self.symbol_table.get_var(children[0].text)
                self.write_push(value["kind"], value["index"])

            elif element.tag == TokensMapping.TokenTypes.KEYWORD:
                if element.text == "null" or element.text == "false":
                    self.write_push("constant", 0)
                elif element.text == "this":
                    self.write_push("pointer", 0)
                elif element.text == "true":
                    self.write_push("constant", 0)
                    self.writeArthimetcs('not')

        elif len(children) == 2:
            self.compile_term(children[1])
            if element.text == '~' or element.text == '-':
                self.process_op(element.text)
        elif len(children) == 3:
            self.compile_expression(children[1])
        elif len(children) == 4:
            value = self.symbol_table.get_var(children[0].text)
            self.write_push(value["kind"], value["index"])
            self.compile_expression(children[2])
        elif len(children) == 6:
            value = self.symbol_table.get_var(children[0].text)
            self.write_push(value["kind"], value["index"])

    def compile_expression(self, element):
        children = list(element)
        self.compile_term(children[0])
        for i in range((len(children) - 1) // 2):
            term = children[i * 2]
            op = children[(i * 2) + 1]
            self.compile_term(term)
            self.process_op(op)

    def process_op(self, op):
        if op == '+':
            self.write("add" + '\n')
        elif op == '-':
            self.write("sub" + '\n')
        elif op == '*':
            self.write("call Math.multiply 2" + '\n')
        elif op == '/':
            self.write("call Math.divide 2" + '\n')
        elif op == '&amp':
            self.write("and" + '\n')
        elif op == '|':
            self.write("or" + '\n')
        elif op == '&lt':
            self.write("lt" + '\n')
        elif op == '&gt':
            self.write("gt" + '\n')
        elif op == '=':
            self.write("eq" + '\n')
        elif op == '-':
            self.write("neg" + '\n')
        elif op == '~':
            self.write("not" + '\n')
