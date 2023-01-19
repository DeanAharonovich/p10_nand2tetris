from JackTokenaizer import JackTokenaizer
import re
from TokensMapping import TokensMapping, TokenTypes

class CompilationEngine:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.tokenaizer = JackTokenaizer(self.input_file)
        self.output_file = open(output_file, "w")
    
    def compileClass(self):
        self.tokenaizer.advance()
        xml = self.process_keyword() 
        xml += self.process_identifier() + self.process_symbol() 
        while self.tokenaizer.current_token in ("static", "field"):
            self.compileClassVarDec()
        while self.tokenaizer.current_token in ("constructor", "function", "method"):
            self.compileSubroutine()
        xml += "</class>\n"
        self.output_file.write(xml)
        return

    def compileClassVarDec(self):
        xml = "<classVarDec>\n"
        xml += self.process_keyword() + self.process_keyword() \
            + self.process_identifier()
        while (self.tokenaizer.current_token == ','):
            xml += self.process_symbol() + self.process_identifier()
        xml += self.process_symbol() #';'
        xml += "<classVarDec>\n"
        return xml

    def compileSubroutine(self):
        xml = "<subroutineDec>\n"
        xml += self.process_keyword()
        if (self.tokenaizer.current_type == TokenTypes.KEYWORD):
            xml += self.process_keyword()
        elif (self.tokenaizer.current_type == TokenTypes.IDENTIFIER):
            xml += self.process_identifier()
        xml += self.process_identifier() + self.process_symbol \
            + self.compileParameterList() \
            + self.process_symbol() + self.process_symbol() \
            + self.compileSubroutineBody() \
            + self.process_symbol() + "</subroutineDec>\n"
        return xml

    def compileParameterList(self):
        xml = "<parameterList>\n"
        while (self.tokenaizer.current_token is not ')'):
            if (self.tokenaizer.current_type == TokenTypes.KEYWORD):
                xml += self.process_keyword()
            elif (self.tokenaizer.current_type == TokenTypes.IDENTIFIER):
                xml += self.process_identifier()
            xml += self.process_identifier()
            if (self.tokenaizer.current_token == ','):
                xml += self.process_symbol()
        xml += "/<parameterList>\n"
        return xml

    def compileSubroutineBody(self):
        xml = "<subroutineBody>\n"
        while self.tokenaizer.current_token() == "var":
            xml += self.compileVarDec()
        xml += self.compileStatements() \
            + "/<subroutineBody>\n"
        return xml

    def compileVarDec(self):
        xml = "<varDec>\n"
        xml += self.process_keyword() + self.process_keyword() \
            + self.process_identifier(self.tokenaizer.current_token)
        while(self.tokenaizer.current_token == ','):
            xml += self.process_symbol() + self.process_identifier()
        xml += self.process_symbol() + "</varDec>\n"
        return xml

    def compileStatements(self):
        xml = "<statements>\n"
        while (self.tokenaizer.current_type == TokenTypes.KEYWORD):
            if (self.tokenaizer.current_token == "let"):
                xml += self.compileLet()
            elif (self.tokenaizer.current_token == "if"):
                xml += self.compileIf()
            elif (self.tokenaizer.current_token == "while"):
                xml += self.compileWhile()
            elif (self.tokenaizer.current_token == "do"):
                xml += self.compileDo()
            elif (self.tokenaizer.current_token == "return"):
                xml += self.compileReturn()
        xml += "</statements>\n"
        return xml

    def compileLet(self):
        xml = "<letStatement>\n"
        xml += self.process_keyword() + self.process_identifier() \
            + self.process_op() + self.compileExpression() + self.process_symbol()
        xml += "</letStatement>\n"
        return xml

    def compileIf(self):
        xml = "<ifStatement>\n"
        xml += self.process_keyword() + self.process_symbol() \
            + self.compileExpression() \
            + self.process_symbol() + self.process_symbol() # if (expression){
        xml += self.compileStatements() + self.process_symbol()
        xml += "</ifStatement>\n"
        return xml

    def compileWhile(self):
        xml = "<whileStatement>\n"
        xml += self.process_keyword() + self.process_symbol() \
            + self.compileExpression() \
            + self.process_symbol() + self.process_symbol() # while (expression){
        xml += self.compileStatements() + self.process_symbol()
        xml += "</whileStatement>\n"
        return xml

    def compileDo(self):
        pass

    def compileReturn(self):
        pass

    def compileExpression(self):
        xml = "<Expression>\n"
        xml += self.compileTerm() 
        while (self.tokenaizer.current_token in TokensMapping.op_list):
            xml += self.process_op() + self.compileTerm()
        xml += "</Expression>\n"
        return xml

    def compileTerm(self): #bookmark 
        xml = "<term>\n"
        if (self.tokenaizer.current_type == TokenTypes.INT):
            xml += self.process_int()
        elif (self.tokenaizer.current_type == TokenTypes.KEYWORD):
            xml += self.process_keyword()
        elif (self.tokenaizer.current_type == TokenTypes.STRING):
            xml += self.process_string()
        elif (self.tokenaizer.current_type == TokenTypes.IDENTIFIER):
            if (self.tokenaizer.nextChar == " "):
                xml += self.process_identifier()
            elif (self.tokenaizer.nextChar == "."):
                xml += self.process_identifier() + self.process_symbol() \
                    + self.process_identifier() + self.process_symbol() \
                    + self.compileExpressionList() + self.process_symbol()
            elif (self.tokenaizer.nextChar == "["):
                xml += self.process_symbol() + self.compileExpression + self.process_symbol()
            elif (self.tokenaizer.nextChar == "("):
                xml += self.process_identifier() + self.process_symbol() \
                    + self.compileExpressionList() + self.process_symbol()
            else:
                xml = "SYNTAX ERROR\n"
        elif (self.tokenaizer.current_type == TokenTypes.SYMBOL):
            if (self.tokenaizer.current_type in ("-", "~")):
                xml += self.process_symbol()
            xml += self.process_symbol() + self.compileExpression() + self.process_symbol()
        else:
            xml = "SYNTAX ERROR\n"
            return xml
        xml += "</term>\n"
        return xml

    def compileExpressionList(self):
        xml = "<epressionList>\n"
        if (self.tokenaizer.current_token is not ")"):
            xml += self.compileExpression()
            while (self.tokenaizer.current_token == ','):
                xml += self.process_symbol() + self.compileExpression()
        xml += "/<epressionList>\n"
        return xml
    
    def process_symbol(self): # need to be changed into different processes to each type.
        if (self.tokenaizer.current_type == TokenTypes.SYMBOL):
            xml = "<symbol> {} </symbol>\n".format(str)
        else:
            xml = "SYNTAX ERROR\n" 
        self.tokenaizer.advance()
        return xml

    def process_keyword(self, str):
        if (self.tokenaizer.current_type == TokenTypes.KEYWORD):
                xml = "<keyword> {} </keyword>\n".format(self.tokenaizer.current_token)
        else:
            xml = "SYNTAX ERROR\n"
        self.tokenaizer.advance()
        return xml

    def process_identifier(self):
        if (self.tokenaizer.current_type == TokenTypes.IDENTIFIER):
            xml = "<identifier> {} </identifier>\n".format(self.tokenaizer.current_token)
        else:
            xml = "SYNTAX ERROR\n"
        self.tokenaizer.advance()
        return xml
    
    def process_string(self):
        if (self.tokenaizer.current_type == TokenTypes.STRING):
            xml = "<stringConst> {} </stringConst>\n".format(self.tokenaizer.current_token)
        else:
            xml = "SYNTAX ERROR\n"
        self.tokenaizer.advance()
        return xml
    
    def process_int(self):
        if (self.tokenaizer.current_type == TokenTypes.INT):
            xml = "<intConst> {} </intConst>\n".format(self.tokenaizer.current_token)
        else:
            xml = "SYNTAX ERROR\n"
        self.tokenaizer.advance()
        return xml

    def process_op(self):
        if (self.tokenaizer.current_type in TokensMapping.op_list):
            xml = "<symbol> {} </symbol>\n".format(self.tokenaizer.current_token)
        else:
            xml = "SYNTAX ERROR\n"
        self.tokenaizer.advance()
        return xml

if __name__ == "__main__":
    x = CompilationEngine("checkIf.txt", "checkIf.xml")
    xml = x.compileIf()
    x.output_file.write(xml)
