from xml.etree import ElementTree

from TokensMapping import LabelTypes
from symbolTable import SymbolTable


class VmWriter:
    def __init__(self, output_file):
        self.output_file = output_file
        self.symbol_table = SymbolTable()

    def compile_vars(self, element):
        """ adds the variables to the symbol table """
        kind, param_type = list(element)[:2]
        for name in list(element)[2:]:
            if name.text == ",":
                continue
            if name.text == ";":
                break
            self.symbol_table.define(name.text, param_type.text, kind.text)

    def write_tree(self, tree: ElementTree.Element, parent=None):
        """ gets a tree element, parsed to tokens, and recursively compiles each part to a vm command. """
        if parent is None:
            self.symbol_table.class_name = tree[1].text

        for element in tree:
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
                self.compile_subroutine(element)

    def compile_subroutine(self, element):
        """ compiles a subroutine element  """
        function_type, *args = element
        if function_type.text == "constructor":
            self.compile_constructor(element)
        elif function_type.text == "function":
            self.compile_function(element)
        else:
            self.compile_method(element)

    def write_if(self, label):
        self.write('if-goto {}'.format(label))

    def write_goto(self, label):
        self.write('goto {}'.format(label))

    def write_label(self, name):
        self.write('label {}'.format(name))

    def write_function(self, class_name, func_name, param_count):
        self.write('function {}.{} {}'.format(class_name, func_name, param_count))

    def write_return(self):
        self.write('return')

    def write_call(self, func_name, arg_count):
        self.write('call {} {}'.format(func_name, arg_count))

    def write_pop(self, segment, offset):
        self.write('pop {0} {1}'.format(segment, offset))

    def write_push(self, segment, offset):
        self.write('push {0} {1}'.format(segment, offset))

    def write(self, vm_line):
        self.output_file.write('{}\n'.format(vm_line))

    def write_constant(self, n):
        self.write_push('constant', n)

    def write_string(self, s):
        """ writes a string by calling string.new and appending each char"""
        s = s[1:-1]
        self.write_constant(len(s))
        self.write_call('String.new', 1)
        for c in s:
            self.write_constant(ord(c))
            self.write_call('String.appendChar', 2)

    def compile_term(self, element, should_push_arg=True):
        """ compiles a term with 1 element depending on its token's type """
        if len(element) == 1:
            child = element[0]
            if child.tag == LabelTypes.INTEGER_CONSTANT:
                self.write_push("constant", child.text)
            elif child.tag == LabelTypes.STRING_CONSTANT:
                self.handle_str(child)
            elif child.tag == LabelTypes.IDENTIFIER:
                value = self.symbol_table.get_var(child.text)
                self.symbol_table.get_var(child.text)
                if value["kind"] != "argument" or should_push_arg:
                    self.write_push(value["kind"], value["index"])
            elif child.tag == LabelTypes.KEYWORD:
                if child.text == "null" or child.text == "false":
                    self.write_push("constant", 0)
                elif child.text == "this":
                    self.write_push("pointer", 0)
                elif child.text == "true":
                    self.write_push("constant", 0)
                    self.process_op('~')

            """ compiles a term with more than 1 element by recursively compile each term  """
        elif len(element) == 2:
            self.compile_term(element[1])
            child = element[0]
            if child.text == "-":
                self.write("neg")
            elif child.text == "~":
                self.process_op(child.text)
        elif len(element) == 3:
            self.compile_expression(element[1])
        elif len(element) == 4:
            if element[1].text == "[":
                self.compile_arr(element[0].text, element[2])
            else:
                self.compile_expression(element[2])
        elif len(element) == 6:
            class_name = element[0]
            function = element[2]
            expression_list = element[4]

            value = self.symbol_table.get_var(class_name.text)
            if value is not None:
                self.write_push(value["kind"], value["index"])
                func_cal = value["type"] + "." + function.text
            else:
                if function.text != "new" and value is not None:
                    self.write_push("pointer", 0)
                func_cal = class_name.text + "." + function.text

            self.compile_expression_list(expression_list)
            arg_count = (len(expression_list) + 1) // 2
            if function.text != "new" and value is not None:
                arg_count += 1
            self.write_call(func_cal, arg_count)

    def compile_expression(self, element, should_push_arg=True):
        """ compiles a n expression by compiling each term """
        children = list(element)
        self.compile_term(children[0], should_push_arg)
        for i in range((len(children) - 1) // 2):
            op = children[1 + (i * 2)]
            term = children[(i * 2) + 2]
            self.compile_term(term, should_push_arg)
            self.process_op(op.text)

    def process_op(self, op):
        if op == '+':
            self.write("add")
        elif op == '-':
            self.write("sub")
        elif op == '*':
            self.write("call Math.multiply 2")
        elif op == '/':
            self.write("call Math.divide 2")
        elif op == '&':
            self.write("and")
        elif op == '|':
            self.write("or")
        elif op == '<':
            self.write("lt")
        elif op == '>':
            self.write("gt")
        elif op == '=':
            self.write("eq")
        elif op == '-':
            self.write("neg")
        elif op == '~':
            self.write("not")

    def compile_constructor(self, element):
        """ compiles a constructor. Using Memory.alloc. Dealing with var dec and statements.
            reset the subroutine table """
        self.symbol_table.reset_subroutine()
        keyword, class_name, func_name, _, param_list, _, body = list(element)
        param_count = (len(list(param_list)) // 3) + 1

        if param_count:
            self.compile_arguments(param_list, True)

        self.write_function(class_name.text, func_name.text, 0)
        self.write("push constant " + str(self.symbol_table.field_index))
        self.write("call Memory.alloc 1")
        self.write("pop pointer 0")  # this
        for var_dec in [tag for tag in list(body) if tag.tag == LabelTypes.CLASS_VAR_DEC]:
            self.compile_vars(var_dec)
        statements = [tag for tag in list(body) if tag.tag == LabelTypes.STATEMENTS][0]
        for statement in statements:
            self.compile_statement(statement)

    def compile_method(self, element):
        """ compiles a method. Reset the subroutine table """
        self.symbol_table.reset_subroutine()
        keyword, return_type, func_name, _, param_list, _, body = list(element)
        param_count = len(list(param_list)) // 2
        if param_count:
            self.compile_arguments(param_list)
        var_tags = [tag for tag in list(body) if tag.tag == LabelTypes.VAR_DEC]
        self.write_function(self.symbol_table.class_name, func_name.text, len(var_tags))
        self.write_push("argument", 0)
        self.write_pop("pointer", 0)
        if param_count:
            self.write_push("argument", param_count)
        for var_dec in var_tags:
            self.compile_vars(var_dec)
        statements = [tag for tag in list(body) if tag.tag == LabelTypes.STATEMENTS][0]
        for statement in statements:
            self.compile_statement(statement, should_pus_arg=param_count == 0)

    def compile_function(self, element):
        """ compiles a function. Reset the subroutine table """
        self.symbol_table.reset_subroutine()
        keyword, return_type, func_name, _, param_list, _, body = list(element)
        param_count = len(list(param_list))
        if param_count:
            self.compile_arguments(param_list)
        for var_dec in [tag for tag in list(body) if tag.tag == LabelTypes.VAR_DEC]:
            self.compile_vars(var_dec)
        self.write_function(self.symbol_table.class_name, func_name.text, self.symbol_table.local_index)
        if return_type.text == "void" and self.symbol_table.class_name != "Main":
            self.write_pop("pointer", 0)
        if return_type.text != "void" and self.symbol_table.class_name != "Main":
            self.write_push("argument", 0)
        statements = [tag for tag in list(body) if tag.tag == LabelTypes.STATEMENTS][0]
        for statement in statements:
            self.compile_statement(statement)

    def compile_statement(self, element, should_pus_arg=True):
        """ compiles a statements regarding the statement's type """
        if element.tag == LabelTypes.LET_STATEMENT:
            self.compile_let(element, should_pus_arg)
        if element.tag == LabelTypes.IF_STATEMENT:
            self.symbol_table.if_counter += 1
            self.compile_if(element, self.symbol_table.if_counter)
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
        elif null_or_expression.tag == LabelTypes.SYMBOL:
            self.write_push("constant", 0)

        self.write_return()

    def compile_do(self, element):
        """ compiles a do statement. Dealing with both function call and class.function call """
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
            self.write_push("pointer", 0)
            self.write_call(self.symbol_table.class_name + '.' + function.text, arg_count + 1)
        else:
            raise Exception("compilation error")

        self.write_pop("temp", 0)

    def compile_while(self, element):
        """ compiles a while statement """
        _, _, while_expression, _, _, statements, _ = element
        counter = self.symbol_table.while_counter
        self.symbol_table.while_counter += 1
        self.write_label("WHILE_EXP" + str(counter))
        self.compile_expression(while_expression)
        self.process_op("~")
        self.write_ifgoto("WHILE_END" + str(counter))
        for statement in statements:
            self.compile_statement(statement)
        self.write_goto("WHILE_EXP" + str(counter))
        self.write_label("WHILE_END" + str(counter))

    def compile_let(self, element, should_pus_arg=True):
        """ compiles a let statement.
            if element's number in statement is >5, handles an array usage. """
        children = list(element)
        if len(children) == 5:
            let, var, equal, expression, semicolon = children
            self.compile_expression(expression, should_pus_arg)
            value = self.symbol_table.get_var(var.text)
            self.write_pop(value["kind"], value["index"])
        else:
            let, var, _, indice, _, equal, expression, semicolon = children
            self.compile_arr(var.text, indice, expression)

    def compile_if(self, element, counter):
        """ compiles an if statement. Handles also with 'else' """
        counter = counter - 1
        children = list(element)
        _if, parentheses, expression, parentheses, brackets, statements, brackets, *else_params = children
        self.compile_expression(expression)
        self.write_if("IF_TRUE{}".format(counter))
        self.write_goto("IF_FALSE{}".format(counter))
        self.write_label("IF_TRUE{}".format(counter))
        for statement in statements:
            self.compile_statement(statement)

        if else_params:
            self.write_goto("IF_END{}".format(counter))
        self.write_label("IF_FALSE{}".format(counter))

        if else_params:
            _, _, statements, _ = else_params
            for statement in statements:
                self.compile_statement(statement)
            self.write_label("IF_END{}".format(counter))

    def compile_arguments(self, element, is_ctor=False):
        """ adds argument to the symbol table """
        for i in range(((len(element) - 1) // 3) + 1):
            var_type = element[i * 3]
            name = element[(i * 3) + 1]
            self.symbol_table.define(name.text, var_type.text, "argument", is_ctor)

    def compile_expression_list(self, expression_list_element):
        for element in expression_list_element:
            if element.tag == LabelTypes.EXPRESSION:
                self.compile_expression(element)

    def write_ifgoto(self, labelname):
        self.write("if-goto " + labelname)

    def compile_arr(self, arr_name, indice_element, expression=None):
        """ compiles an array usage. Handles the index expression and the assignment expression, if exists. """
        row = self.symbol_table.get_var(arr_name)
        self.compile_expression(indice_element)
        self.write_push(row["kind"], row["index"])
        self.process_op('+')
        if expression:
            self.compile_expression(expression)
            self.write_pop("temp", 0)
            self.write_pop("pointer", 1)
            self.write_push("temp", 0)
            self.write_pop("that", 0)
        else:
            self.write_pop("pointer", 1)
            self.write_push("that", 0)
