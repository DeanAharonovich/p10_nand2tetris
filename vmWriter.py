from xml.etree import ElementTree

from TokensMapping import LabelTypes
from symbolTable import SymbolTable

kind_to_segment = {'static': 'static',
                   'field': 'this',
                   'arg': 'argument',
                   'var': 'local'}


class vmWriter:
    def __init__(self, output_file):
        self.output_file = output_file
        self.label_count = 0
        self.symbol_table = SymbolTable()

    def compile_vars(self, element):
        kind, type = list(element)[:2]
        for name in list(element)[2:]:
            if name.text == ",":
                continue
            if name.text == ";":
                break
            self.symbol_table.define(name.text, type.text, kind.text)

    def write_tree(self, element: ElementTree.Element, parent=None):
        if parent is None:
            self.symbol_table.class_name = element[1].text
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
        if element.tag == LabelTypes.SUBROUTINE_DEC:
            self.compile_function(element)

        for child in element:
            self.write_tree(child, element)

    def compile_function(self, element):
        function_type, *args = element
        if function_type.text == "constructor":
            self.compile_constructor(element)
        else:
            self.compile_subroutine(element)

    def write_if(self, label):
        self.output_file.write('not\n')  # Negate to jump if the conditions doesn't hold
        self.output_file.write('if-goto {}\n'.format(label))

    def write_goto(self, label):
        self.output_file.write('goto {}\n'.format(label))

    def write_label(self, label):
        self.output_file.write('label {}\n'.format(label))

    def write_function(self, class_name, func_name, param_count):
        self.output_file.write('function {}.{} {}\n'.format(class_name, func_name, param_count))

    def write_return(self):
        self.output_file.write('return\n')

    def write_call(self, func_name, arg_count):
        self.output_file.write('call {} {}\n'.format(
            func_name, arg_count
        ))

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
            if child.tag == LabelTypes.INTEGER_CONSTANT:
                self.write_push("constant", child.text)

            elif child.tag == LabelTypes.STRING_CONSTANT:
                self.handle_str(child)

            elif element.tag == LabelTypes.IDENTIFIER:
                value = self.symbol_table.get_var(children[0].text)
                self.write_push(value["kind"], value["index"])

            elif element.tag == LabelTypes.KEYWORD:
                if element.text == "null" or element.text == "false":
                    self.write_push("constant", 0)
                elif element.text == "this":
                    self.write_push("pointer", 0)
                elif element.text == "true":
                    self.write_push("constant", 0)
                    self.process_op('~')

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
            expression_list= children[4]
            self.compile_expression_list(expression_list)
            arg_count = (len(expression_list) + 1) // 2
            self.write_call(children[0].text+"."+children[2].text, arg_count)

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
        elif op == '&':
            self.write("and" + '\n')
        elif op == '|':
            self.write("or" + '\n')
        elif op == '<':
            self.write("lt" + '\n')
        elif op == '>':
            self.write("gt" + '\n')
        elif op == '=':
            self.write("eq" + '\n')
        elif op == '-':
            self.write("neg" + '\n')
        elif op == '~':
            self.write("not" + '\n')

    def handle_str(self, element):
        string = element.text
        self.write_push("constant", len(string))
        self.write_call("String.new", 1)
        for i in string:
            self.write_push("constant", ord(i))
            self.write_call("String.appendChar", 2)

    def compile_subroutine(self, element):
        keyword, class_name, func_name, _, param_list, _, body = list(element)
        param_count = len(list(param_list))
        self.write_function(class_name.text, func_name.text, param_count)
        statements = list(list(body)[1])
        for statement in statements:
            self.compile_statement(statement)

    def compile_statement(self, element):
        if element.tag == LabelTypes.LET_STATEMENT:
            self.compile_let(element)
        if element.tag == LabelTypes.IF_STATEMENT:
            self.compile_if(element)
        if element.tag == LabelTypes.WHILE_STATEMENT:
            self.compile_while(element)
        if element.tag == LabelTypes.DO_STATEMENT:
            self.compile_do(element)
        if element.tag == LabelTypes.RETURN_STATEMENT:
            self.compile_return(element)

    def compile_return(self, element):
        _, null_or_expression, *args = list(element)
        if null_or_expression.tag == LabelTypes.EXPRESSION:
            self.compile_expression(null_or_expression)
        else:
            self.write_push("constant", 0)
        self.write_return()

    def compile_do(self, element):
        do, *children = element
        if len(children) == 7:
            do, class_name, point, function, _, expression_list, _, _ = element
            value = self.symbol_table.get_var(class_name.text)
            if value is not None:  # an object
                self.write_push(value["kind"], value["index"])
                func_cal = value["type"] + "." + function.text
            else:
                func_cal = class_name.text + "." + function.text
            arg_count = (len(expression_list) + 1) // 2
            self.compile_expression_list(expression_list)

            if value is not None:
                self.write_call(func_cal, arg_count + 1)
            else:
                self.write_call(func_cal, arg_count)

        elif len(children) == 5:
            do, function, _, expression_list, _, _ = element
            arg_count = (len(expression_list) + 1) // 2

            if function.text in self.symbol_table.methods:
                self.write_push("pointer", 0)
                arg_count += 1
            self.compile_expression_list(expression_list)
            self.write_call(self.symbol_table.class_name + '.' + function.text, arg_count)
        else:
            pass

        self.write_pop("temp", 0)

    def compile_while(self, element):
        pass

    def compile_let(self, element):
        children = list(element)

        if len(children) == 5:
            let, var, equal, expression, semicolon = children
            self.compile_expression(expression)
            value = self.symbol_table.get_var(var.text)
            self.write_pop(value["kind"], value["index"])
        else:
            pass  # array

    def compile_if(self, element):
        pass

    def compile_constructor(self, element):
        self.symbol_table.subroutine_var_dec = {}
        keyword, class_name, func_name, _, param_list, _, body = list(element)
        param_count = len(list(param_list))

        if param_count:
            self.compile_arguments()

        self.write_function(class_name.text, func_name.text, param_count)
        self.output_file.write("push constant " + str(self.symbol_table.field_index) + '\n')
        self.output_file.write("call Memory.alloc 1" + '\n')
        self.output_file.write("pop pointer 0" + '\n')  # this
        statements = list(list(body)[1])
        for statement in statements:
            self.compile_statement(statement)

    def compile_arguments(self):
        pass

    def compile_expression_list(self, expression_list_element):
        for element in expression_list_element:
            if element.tag == LabelTypes.EXPRESSION:
                self.compile_expression(element)
        