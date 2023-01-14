from JackTokenaizer import JackTokenaizer

class CompilationEngine:
    def __init__(self, token: JackTokenaizer):
        self.current_token = token.current_token
    
    def compile_if(self):
        xml = "<ifStatement>\n"
        xml += self.process("if") + self.process("(") + self.compile_expression() \
            + self.process(")") + self.process("\{") + self.compile_statements() + self.process("\}")
        xml += "</ifStatement>\n"
        return xml

    def process(self ,str):
        if (str == self.current_token):
            xml = "<keyword> {} </keyword>\n".format(str)
        else:
            xml = "SYNTAX ERROR"
        self.current_token.advance()