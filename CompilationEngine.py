from JackTokenaizer import JackTokenaizer

class CompilationEngine:
    def __init__(self, input_file, output_file):
        self.tokenaizer = JackTokenaizer(input_file)
        self.output_file = open(output_file, "w")
    
    def compileClass(self):
        xml = self.process("class")
        xml += self.process("(") + self.compileExpression() \
            + self.process(")") + self.process("{") + self.compileStatements() + self.process("}")
        xml += "</ifStatement>\n"
        self.output_file.write(xml)
        return

    def compileClassVarDec(self):
        pass

    def compileSubroutine(self):
        pass

    def compileParameterList(self):
        pass

    def compileSubroutineBody(self):
        pass

    def compileVarDec(self):
        pass

    def compileStatements(self):
        pass

    def compileLet(self):
        pass

    def compileIf(self):
        xml = "<ifStatement>\n"
        xml += self.process("if") + self.process("(") + self.compileExpression() \
            + self.process(")") + self.process("{") + self.compileStatements() + self.process("}")
        xml += "</ifStatement>\n"
        self.output_file.write(xml)
        return

    def compileWhile(self):
        xml = "<whileStatement>\n"
        xml += self.process("while") + self.process("(") + self.compileExpression() \
            + self.process(")") + self.process("\{") + self.compileStatements() + self.process("\}")
        xml += "</whileStatement>\n"
        self.output_file.write(xml)
        return

    def compileDo(self):
        pass

    def compileReturn(self):
        pass

    def compileExpression(self):
        xml = "<Expression>\n"
        xml += "<term>\n"
        xml +=

    def compileTerm(self):
        pass

    def compileExpressionList(self):
        pass
    
    def process(self ,str):
        if (str == self.tokenaizer.current_token): #(self.tokenaizer.current_type == "SYMBOL") and
            xml = "<keyword> {} </keyword>\n".format(str)
        else:
            xml = "SYNTAX ERROR"
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