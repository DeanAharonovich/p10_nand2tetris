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
        xml = self.process("class")
        xml += self.process(self.tokenaizer.current_token) + self.process("{") \
            + self.compileClassVarDec()
        xml += "</ifStatement>\n"
        return xml

    def compileClassVarDec(self):
        pass

    def compileSubroutine(self):
        pass

    def compileParameterList(self):
        pass

    def compileSubroutineBody(self):
        pass

    def compileVarDec(self):
        xml = "<varDec>\n"
        xml += self.process("var") + self.process(self.tokenaizer.current_token) + self.process(self.tokenaizer.current_token)
        while(self.tokenaizer.current_token == ','):
            xml += self.process(",") \
                + self.process(self.tokenaizer.current_token)
        xml += self.process(";") + "\n</varDec>\n"
        return xml

    def compileStatements(self):
        xml = "<statements>\n"
        while (self.tokenaizer.current_type == TokenTypes.symbol):
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
        xml += self.process("let") + self.process(self.tokenaizer.current_token) \
            + self.process("=") + self.compileExpression() + self.process(";")
        xml += "</letStatement>\n"
        return xml

    def compileIf(self):
        self.tokenaizer.advance()
        xml = "<ifStatement>\n"
        xml += self.process("if") \
            + self.process("(") \
            + self.compileTerm() \
            + self.process(")") + self.process("{") \
            + self.compileStatements() + self.process("}")
        xml += "\n</ifStatement>\n"
        return xml

    def compileWhile(self):
        xml = "<whileStatement>\n"
        xml += self.process("while") + self.process("(") + self.compileTerm() \
            + self.process(")") + self.process("\{") + self.compileStatements() + self.process("\}")
        xml += "</whileStatement>\n"
        return xml

    def compileDo(self):
        pass

    def compileReturn(self):
        pass

    def compileExpression(self):
        xml = "<Expression>\n"
        xml += self.compileTerm() 
        while (self.tokenaizer.current_type == TokenTypes.SYMBOL and \
               self.tokenaizer.current_token in TokensMapping.op_list):
               xml += self.process_op(self.tokenaizer.current_token) \
                   + self.compileTerm()
        xml += "\n</Expression>\n"
        return xml

    def compileTerm(self): #bookmark
        xml = "<term>\n"
        if (self.tokenaizer.current_type == TokenTypes.INT):
            xml += "<intConst> {} </intConst>\n".format(self.tokenaizer.current_token)
        elif (self.tokenaizer.current_type == TokenTypes.KEYWORD):
            xml += "<keyword> {} </keyword>\n".format(self.tokenaizer.current_token)
        elif (self.tokenaizer.current_type == TokenTypes.STRING):
            xml += "<stringConst> {} </stringConst>\n".format(self.tokenaizer.current_token)
        elif (self.tokenaizer.current_type == TokenTypes.IDENTIFIER):
            if (self.tokenaizer.nextChar == " "):
                xml += "<identifier> {} </identifier>\n".format(self.tokenaizer.current_token)
            elif (self.tokenaizer.nextChar == "."):
                pass
            elif (self.tokenaizer.nextChar == "["):
                pass
            elif (self.tokenaizer.nextChar == "("):
                pass
            elif (self.tokenaizer.nextChar == " "):
                pass
        else:
            xml = "SYNTAX ERROR"
            return xml
        xml += "</term>\n"
        self.tokenaizer.advance()
        return xml

    def compileExpressionList(self):
        pass
    
    def process(self ,str): # need to be changed into different processes to each type.
        if (str == self.tokenaizer.current_token):
            if (self.tokenaizer.current_type == TokenTypes.SYMBOL):
                xml = "<symbol> {} </symbol>\n".format(str)
            elif (self.tokenaizer.current_type == TokenTypes.KEYWORD):
                xml = "<keyword> {} </keyword>\n".format(str)
            elif (self.tokenaizer.current_type == TokenTypes.IDENTIFIER):
                xml = "<identifier> {} </identifier>\n".format(str)
            elif (self.tokenaizer.current_type == TokenTypes.INT):
                xml = "<intConst> {} </intConst>\n".format(str)
            elif (self.tokenaizer.current_type == TokenTypes.STRING):
                xml = "<stringConst> {} </stringConst>\n".format(str)
            else:
                xml = "ERROR - TOKEN IS NOT IN TOKEN'S LIST"
        else:
            xml = "ERROR - SYNTAX ERROR"
        self.tokenaizer.advance()
        return xml

    """def processIdentifier(self):
        if (self.tokenaizer.tokenType == "IDENTIFIER"):
            xml = "<identifier> {} </identifier>\n".format(self.tokenaizer.current_token)
        else:
            xml = "SYNTAX ERROR"
        self.tokenaizer.advance()
        return xml
    
    def processString(self):
        if (self.tokenaizer.tokenType == "STRING"):
            xml = "<stringConst> {} </stringConst>\n".format(self.tokenaizer.current_token)
        else:
            xml = "SYNTAX ERROR"
        self.tokenaizer.advance()
        return xml
    
    def processInt(self):
        if (self.tokenaizer.tokenType == "INTCONST"):
            xml = "<intConst> {} </intConst>\n".format(self.tokenaizer.current_token)
        else:
            xml = "SYNTAX ERROR"
        self.tokenaizer.advance()
        return xml"""

    def process_op(self):
        if (self.tokenaizer.current_type in TokensMapping.op_list):
            xml = "<symbol> {} </symbol>\n".format(self.tokenaizer.current_token)
        else:
            xml = "SYNTAX ERROR"
        self.tokenaizer.advance()
        return xml

if __name__ == "__main__":
    x = CompilationEngine("checkIf.txt", "checkIf.xml")
    xml = x.compileIf()
    x.output_file.write(xml)
