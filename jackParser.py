from xml.etree.ElementTree import Element

from JackTokenaizer import JackTokenaizer
from TokensMapping import TokensMapping, TokenTypes, LabelTypes


class JackParser:
    def __init__(self, input_file):
        self.input_file = input_file
        self.tokenizer = JackTokenaizer(self.input_file)

    def compile_class(self):
        """ parsing a complete class to a tree element """
        class_element = Element('class')

        self.tokenizer.advance()
        class_element.append(self.process_keyword())
        class_element.append(self.process_identifier())
        class_element.append(self.process_symbol())

        while self.tokenizer.current_token in ("static", "field"):
            class_element.append(self.compile_var_dec_generic(LabelTypes.CLASS_VAR_DEC))
        while self.tokenizer.current_token in ("constructor", "function", "method"):
            class_element.append(self.compile_subroutine())

        class_element.append(self.process_symbol())

        return class_element

    def compile_var_dec_generic(self, var_dec_type):
        """ parsing a var declaration to an element """
        var_dec_element = Element(var_dec_type)
        var_dec_element.append(self.process_keyword())

        if self.tokenizer.current_type == TokenTypes.KEYWORD:
            var_dec_element.append(self.process_keyword())
        else:
            var_dec_element.append(self.process_identifier())

        var_dec_element.append(self.process_identifier())

        while self.tokenizer.current_token == ',':
            var_dec_element.append(self.process_symbol())
            var_dec_element.append(self.process_identifier())

        var_dec_element.append(self.process_symbol())
        return var_dec_element

    def compile_subroutine(self):
        """ parsing a sub to a tree_element """
        subroutine_element = Element(LabelTypes.SUBROUTINE_DEC)
        subroutine_element.append(self.process_keyword())

        if self.tokenizer.current_type == TokenTypes.KEYWORD:
            subroutine_element.append(self.process_keyword())
        elif self.tokenizer.current_type == TokenTypes.IDENTIFIER:
            subroutine_element.append(self.process_identifier())

        subroutine_element.append(self.process_identifier())
        subroutine_element.append(self.process_symbol())
        subroutine_element.append(self.compile_parameter_list())
        subroutine_element.append(self.process_symbol())
        subroutine_element.append(self.compile_subroutine_body())
        return subroutine_element

    def compile_parameter_list(self):
        """ parsing a parameter list to tree_element """
        param_list_element = Element(LabelTypes.PARAMETER_LIST)

        while self.tokenizer.current_token != ')':
            if self.tokenizer.current_type == TokenTypes.KEYWORD:
                param_list_element.append(self.process_keyword())
            elif self.tokenizer.current_type == TokenTypes.IDENTIFIER:
                param_list_element.append(self.process_identifier())
            param_list_element.append(self.process_identifier())
            if self.tokenizer.current_token == ',':
                param_list_element.append(self.process_symbol())
        return param_list_element

    def compile_subroutine_body(self):
        """ parsing a sub_body to tree_element """
        sub_body_element = Element(LabelTypes.SUBROUTINE_BODY)
        sub_body_element.append(self.process_symbol())
        while self.tokenizer.current_token == "var":
            sub_body_element.append(self.compile_var_dec_generic(LabelTypes.VAR_DEC))
        sub_body_element.append(self.compile_statements())
        sub_body_element.append(self.process_symbol())
        return sub_body_element

    def compile_statements(self):
        """ parsing a statement to tree_element """
        statements_element = Element(LabelTypes.STATEMENTS)

        while self.tokenizer.current_type == TokenTypes.KEYWORD:
            if self.tokenizer.current_token == "let":
                statements_element.append(self.compile_let())
            elif self.tokenizer.current_token == "if":
                statements_element.append(self.compile_if())
            elif self.tokenizer.current_token == "while":
                statements_element.append(self.compile_while())
            elif self.tokenizer.current_token == "do":
                statements_element.append(self.compile_do())
            elif self.tokenizer.current_token == "return":
                statements_element.append(self.compile_return())
        return statements_element

    def compile_let(self):
        """ parsing a let statement to tree_element """
        let_element = Element(LabelTypes.LET_STATEMENT)
        let_element.append(self.process_keyword())
        let_element.append(self.process_identifier())
        if self.tokenizer.current_token == "[":
            let_element.append(self.process_symbol())
            let_element.append(self.compile_expression())
            let_element.append(self.process_symbol())
        let_element.append(self.process_op())
        let_element.append(self.compile_expression())
        let_element.append(self.process_symbol())
        return let_element

    def compile_if(self):
        """ parsing a if statement to tree_element """
        if_element = Element(LabelTypes.IF_STATEMENT)
        if_element.append(self.process_keyword())
        if_element.append(self.process_symbol())
        if_element.append(self.compile_expression())
        if_element.append(self.process_symbol())
        if_element.append(self.process_symbol())
        if_element.append(self.compile_statements())
        if_element.append(self.process_symbol())

        if self.tokenizer.current_token == "else":
            if_element.append(self.process_keyword())
            if_element.append(self.process_symbol())
            if_element.append(self.compile_statements())
            if_element.append(self.process_symbol())

        return if_element

    def compile_while(self):
        """ parsing a while statement to tree_element """
        while_element = Element(LabelTypes.WHILE_STATEMENT)
        while_element.append(self.process_keyword())
        while_element.append(self.process_symbol())
        while_element.append(self.compile_expression())
        while_element.append(self.process_symbol())
        while_element.append(self.process_symbol())
        while_element.append(self.compile_statements())
        while_element.append(self.process_symbol())
        return while_element

    def compile_do(self):
        """ parsing a do statement to tree_element """
        do_element = Element(LabelTypes.DO_STATEMENT)
        do_element.append(self.process_keyword())

        if self.tokenizer.nextChar() == ".":
            do_element.append(self.process_identifier())
            do_element.append(self.process_symbol())
            do_element.append(self.process_identifier())
            do_element.append(self.process_symbol())
            do_element.append(self.compile_expression_list())
            do_element.append(self.process_symbol())

        elif self.tokenizer.nextChar() == "(":
            do_element.append(self.process_identifier())
            do_element.append(self.process_symbol())
            do_element.append(self.compile_expression_list())
            do_element.append(self.process_symbol())

        else:
            raise Exception("Excpected {}, got {} instead".format("'.' or '('", self.tokenizer.nextChar()))

        do_element.append(self.process_symbol())
        return do_element

    def compile_return(self):
        """ parsing a return statement to tree_element """
        return_element = Element(LabelTypes.RETURN_STATEMENT)
        return_element.append(self.process_keyword())

        if self.tokenizer.current_token != ";":
            return_element.append(self.compile_expression())
        return_element.append(self.process_symbol())
        return return_element

    def compile_expression(self):
        """ parsing an expression to a tree_element """
        expression_element = Element(LabelTypes.EXPRESSION)
        expression_element.append(self.compile_term())
        while self.tokenizer.current_token in TokensMapping.op_list:
            expression_element.append(self.process_op())
            expression_element.append(self.compile_term())
        return expression_element

    def compile_term(self):
        """ parsing a term to atree_element """
        term_element = Element(LabelTypes.TERM)
        if self.tokenizer.current_type == TokenTypes.INT:
            term_element.append(self.process_int())
        elif self.tokenizer.current_type == TokenTypes.KEYWORD:
            term_element.append(self.process_keyword())
        elif self.tokenizer.current_type == TokenTypes.STRING:
            term_element.append(self.process_string())
        elif self.tokenizer.current_type == TokenTypes.IDENTIFIER:
            if self.tokenizer.nextChar() in [" ", ")", "]", ";", ",", "=", "/"]:
                term_element.append(self.process_identifier())
            elif self.tokenizer.nextChar() == ".":
                term_element.append(self.process_identifier())
                term_element.append(self.process_symbol())
                term_element.append(self.process_identifier())
                term_element.append(self.process_symbol())
                term_element.append(self.compile_expression_list())
                term_element.append(self.process_symbol())

            elif self.tokenizer.nextChar() in ["[", "("]:
                term_element.append(self.process_identifier())
                term_element.append(self.process_symbol())
                term_element.append(self.compile_expression())
                term_element.append(self.process_symbol())
            else:
                raise Exception(
                    "Excpected {}, got {} instead".format(["(,[, ' ', ), ] ; ,"], self.tokenizer.nextChar()))
        elif self.tokenizer.current_type == TokenTypes.SYMBOL:
            if self.tokenizer.current_token in ("-", "~"):
                term_element.append(self.process_symbol())
                term_element.append(self.compile_term())
            if self.tokenizer.current_token == "(":
                term_element.append(self.process_symbol())
                term_element.append(self.compile_expression())
                term_element.append(self.process_symbol())

        else:
            raise Exception("invalid symbol type : {}".format(self.tokenizer.current_type))

        return term_element

    def compile_expression_list(self):
        expression_list_element = Element(LabelTypes.EXPRESSION_LIST)
        if self.tokenizer.current_token != ")":
            expression_list_element.append(self.compile_expression())
            while self.tokenizer.current_token == ',':
                expression_list_element.append(self.process_symbol())
                expression_list_element.append(self.compile_expression())
        return expression_list_element

    def process_symbol(self):
        if self.tokenizer.current_type == TokenTypes.SYMBOL:
            element = Element(LabelTypes.SYMBOL)
            element.text = self.tokenizer.current_token
            self.tokenizer.advance()
            return element
        else:
            raise Exception("Expected {}, got {} instead".format(TokenTypes.SYMBOL, self.tokenizer.current_type))

    def process_keyword(self):
        if self.tokenizer.current_type == TokenTypes.KEYWORD:
            element = Element(LabelTypes.KEYWORD)
            element.text = self.tokenizer.current_token
            self.tokenizer.advance()
            return element
        else:
            raise Exception("Expected {}, got {} instead".format(TokenTypes.KEYWORD, self.tokenizer.current_type))

    def process_identifier(self):
        if self.tokenizer.current_type == TokenTypes.IDENTIFIER:
            element = Element(LabelTypes.IDENTIFIER)
            element.text = self.tokenizer.current_token
            self.tokenizer.advance()
            return element
        else:
            raise Exception("Expected {}, got {} instead".format(TokenTypes.IDENTIFIER, self.tokenizer.current_type))

    def process_string(self):
        if self.tokenizer.current_type == TokenTypes.STRING:
            element = Element(LabelTypes.STRING_CONSTANT)
            element.text = self.tokenizer.current_token
            self.tokenizer.advance()
            return element
        else:
            raise Exception("Expected {}, got {} instead".format(TokenTypes.STRING, self.tokenizer.current_type))

    def process_int(self):
        if self.tokenizer.current_type == TokenTypes.INT:
            element = Element(LabelTypes.INTEGER_CONSTANT)
            element.text = self.tokenizer.current_token
            self.tokenizer.advance()
            return element
        else:
            raise Exception("Expected {}, got {} instead".format(TokenTypes.INT, self.tokenizer.current_type))

    def process_op(self):
        if self.tokenizer.current_token in TokensMapping.op_list:
            element = Element(LabelTypes.SYMBOL)
            element.text = self.tokenizer.current_token
            self.tokenizer.advance()
            return element
        else:
            raise Exception(
                "Expected one of {}, got {} instead".format(TokensMapping.op_list, self.tokenizer.current_token))
