from JackTokenaizer import JackTokenaizer
from TokensMapping import TokensMapping, TokenTypes


# create XML 
class CompilationEngine:
    def __init__(self, input_file):
        self.input_file = input_file
        self.tokenizer = JackTokenaizer(self.input_file)

    def compile_class(self):
        xml = "<class>\n"
        self.tokenizer.advance()
        xml += self.process_keyword()
        xml += self.process_identifier() + self.process_symbol()
        while self.tokenizer.current_token in ("static", "field"):
            xml += self.compileClassVarDec()
        while self.tokenizer.current_token in ("constructor", "function", "method"):
            xml += self.compileSubroutine()
        xml += self.process_symbol()

        xml += "</class>\n"
        return xml

    def compileClassVarDec(self):
        xml = "<classVarDec>\n"
        xml += self.process_keyword()
        if self.tokenizer.current_type == TokenTypes.KEYWORD:
            xml += self.process_keyword()
        else:
            xml += self.process_identifier()

        xml += self.process_identifier()
        while (self.tokenizer.current_token == ','):
            xml += self.process_symbol() + self.process_identifier()
        xml += self.process_symbol()  # ';'
        xml += "</classVarDec>\n"
        return xml

    def compileSubroutine(self):
        xml = "<subroutineDec>\n"
        xml += self.process_keyword()
        if self.tokenizer.current_type == TokenTypes.KEYWORD:
            xml += self.process_keyword()
        elif self.tokenizer.current_type == TokenTypes.IDENTIFIER:
            xml += self.process_identifier()
        xml += self.process_identifier() + self.process_symbol() \
               + self.compileParameterList() \
               + self.process_symbol() \
               + self.compileSubroutineBody() \
               + "</subroutineDec>\n"
        return xml

    def compileParameterList(self):
        xml = "<parameterList>\n"
        while (self.tokenizer.current_token != ')'):
            if (self.tokenizer.current_type == TokenTypes.KEYWORD):
                xml += self.process_keyword()
            elif (self.tokenizer.current_type == TokenTypes.IDENTIFIER):
                xml += self.process_identifier()
            xml += self.process_identifier()
            if (self.tokenizer.current_token == ','):
                xml += self.process_symbol()
        xml += "</parameterList>\n"
        return xml

    def compileSubroutineBody(self):
        xml = "<subroutineBody>\n"
        xml += self.process_symbol()
        while self.tokenizer.current_token == "var":
            xml += self.compileVarDec()
        xml += self.compileStatements() + self.process_symbol() + "</subroutineBody>\n"
        return xml

    def compileVarDec(self):
        xml = "<varDec>\n"
        xml += self.process_keyword() + self.process_keyword() \
               + self.process_identifier()
        while (self.tokenizer.current_token == ','):
            xml += self.process_symbol() + self.process_identifier()
        xml += self.process_symbol() + "</varDec>\n"
        return xml

    def compileStatements(self):
        xml = "<statements>\n"
        while self.tokenizer.current_type == TokenTypes.KEYWORD:
            if self.tokenizer.current_token == "let":
                xml += self.compileLet()
            elif self.tokenizer.current_token == "if":
                xml += self.compileIf()
            elif self.tokenizer.current_token == "while":
                xml += self.compileWhile()
            elif self.tokenizer.current_token == "do":
                xml += self.compileDo()
            elif self.tokenizer.current_token == "return":
                xml += self.compileReturn()
        xml += "</statements>\n"
        return xml

    def compileLet(self):
        xml = "<letStatement>\n"
        xml += self.process_keyword() + self.process_identifier() + self.process_op() + self.compileExpression() + self.process_symbol()
        xml += "</letStatement>\n"
        return xml

    def compileIf(self):
        xml = "<ifStatement>\n"
        xml += self.process_keyword() + self.process_symbol() \
               + self.compileExpression() \
               + self.process_symbol() + self.process_symbol()  # if (expression){
        xml += self.compileStatements() + self.process_symbol()
        xml += "</ifStatement>\n"
        return xml

    1 * (2 * 3)

    def compileWhile(self):
        xml = "<whileStatement>\n"
        xml += self.process_keyword() + self.process_symbol() \
               + self.compileExpression() \
               + self.process_symbol() + self.process_symbol()  # while (expression){
        xml += self.compileStatements() + self.process_symbol()
        xml += "</whileStatement>\n"
        return xml

    def compileDo(self):
        xml = "<doStatement>\n"
        xml += self.process_keyword()
        if (self.tokenizer.nextChar() == "."):
            xml += self.process_identifier() + self.process_symbol() \
                   + self.process_identifier() + self.process_symbol() \
                   + self.compileExpressionList() + self.process_symbol()
        elif (self.tokenizer.nextChar() == "("):
            xml += self.process_identifier() + self.process_symbol() \
                   + self.compileExpressionList() + self.process_symbol()
        else:
            xml = "SYNTAX ERROR\n"
        xml += self.process_symbol()
        xml += "</doStatement>\n"
        return xml

    def compileReturn(self):
        xml = "<returnStatement>\n"
        xml += self.process_keyword()
        if self.tokenizer.current_token != ";":
            xml += self.compileExpression()
        xml += self.process_symbol()
        xml += "</returnStatement>\n"
        return xml

    def compileExpression(self):
        xml = "<expression>\n"
        xml += self.compileTerm()
        while (self.tokenizer.current_token in TokensMapping.op_list):
            xml += self.process_op() + self.compileTerm()
        xml += "</expression>\n"
        return xml

    def compileTerm(self):  # bookmark 
        xml = "<term>\n"
        if (self.tokenizer.current_type == TokenTypes.INT):
            xml += self.process_int()
        elif (self.tokenizer.current_type == TokenTypes.KEYWORD):
            xml += self.process_keyword()
        elif (self.tokenizer.current_type == TokenTypes.STRING):
            xml += self.process_string()
        elif (self.tokenizer.current_type == TokenTypes.IDENTIFIER):
            if (self.tokenizer.nextChar() in [" ", ")"]):
                xml += self.process_identifier()
            elif (self.tokenizer.nextChar() == "."):
                xml += self.process_identifier() + self.process_symbol() \
                       + self.process_identifier() + self.process_symbol() \
                       + self.compileExpressionList() + self.process_symbol()
            elif (self.tokenizer.nextChar() == "["):
                xml += self.process_symbol() + self.compileExpression() + self.process_symbol()
            elif (self.tokenizer.nextChar() == "("):
                xml += self.process_identifier() + self.process_symbol() \
                       + self.compileExpressionList() + self.process_symbol()
            else:
                xml = "SYNTAX ERROR\n"
        elif self.tokenizer.current_type == TokenTypes.SYMBOL:
            if self.tokenizer.current_token in ("-", "~"):
                xml += self.process_symbol()
                xml += self.compileTerm()
            if self.tokenizer.current_token == "(":
                xml += self.process_symbol() + self.compileExpression() + self.process_symbol()



        else:
            xml = "SYNTAX ERROR\n"
            return xml
        xml += "</term>\n"
        return xml

    def compileExpressionList(self):
        xml = "<expressionList>\n"
        if self.tokenizer.current_token != ")":
            xml += self.compileExpression()
            while (self.tokenizer.current_token == ','):
                xml += self.process_symbol() + self.compileExpression()
        xml += "</expressionList>\n"
        return xml

    def process_symbol(self):  # need to be changed into different processes to each type.
        if (self.tokenizer.current_type == TokenTypes.SYMBOL):
            xml = "<symbol> {} </symbol>\n".format(self.tokenizer.current_token)
        else:
            xml = "SYNTAX ERROR\n"
        self.tokenizer.advance()
        return xml

    def process_keyword(self):
        if (self.tokenizer.current_type == TokenTypes.KEYWORD):
            xml = "<keyword> {} </keyword>\n".format(self.tokenizer.current_token)
        else:
            xml = "SYNTAX ERROR\n"
        self.tokenizer.advance()
        return xml

    def process_identifier(self):
        if (self.tokenizer.current_type == TokenTypes.IDENTIFIER):
            xml = "<identifier> {} </identifier>\n".format(self.tokenizer.current_token)
        else:
            xml = "SYNTAX ERROR\n"
        self.tokenizer.advance()
        return xml

    def process_string(self):
        if (self.tokenizer.current_type == TokenTypes.STRING):
            xml = "<stringConst> {} </stringConst>\n".format(self.tokenizer.current_token)
        else:
            raise Exception("Excpected {}, got {} instead".format(TokenTypes.STRING,
                                                                  self.tokenizer.current_type))  # todo consolidate
        self.tokenizer.advance()
        return xml

    def process_int(self):
        if (self.tokenizer.current_type == TokenTypes.INT):
            xml = "<integerConstant> {} </integerConstant>\n".format(self.tokenizer.current_token)
        else:
            xml = "SYNTAX ERROR\n"
        self.tokenizer.advance()
        return xml

    def process_op(self):
        if (self.tokenizer.current_token in TokensMapping.op_list):
            xml = "<symbol> {} </symbol>\n".format(self.tokenizer.current_token)
        else:
            xml = "SYNTAX ERROR\n"
        self.tokenizer.advance()
        return xml



