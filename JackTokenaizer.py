import re
from TokensMapping import TokensMapping
from CompilationEngine import CompilationEngine

class JackTokenaizer:
    def __init__(self, inputFile):
        self.current_token = None
        self.current_type = None
        #self.symbols = re.compile("[{}()\[\].,;+\-*\/&|<>=~]")
        #self.keywords = re.compile("""(class|constructor|function|method|field|static|var|int|char|
        #                              boolean|void|true|false|null|this|let|do|if|else|while|return)""")
        #self.integerConst = re.compile("\b\d+\b")
        #self.string = re.compile("[\"](.*)[\"]")
        #self.identifier = re.compile("\b[A-Za-z_][A-Za-z_0-9]*\b")
        self.in_file = open(inputFile, "r")
        self.current_line = None
        self.current_loc_in_line = 0

    def advance(self):
        
        if self.current_line:
            exp = ""
            exp += self.current_line[self.current_loc_in_line]
            if (exp in TokensMapping.symbols):
                self.current_token = exp
                self.current_type = TokensMapping.token_type[0]
                exp = ""
            
            elif (exp in TokensMapping.keywords):
                self.current_token = exp
                self.current_type = TokensMapping.token_type[1]
                exp = ""
            
            elif (exp in TokensMapping.cons_int):
                while (isinstance(self.current_line[self.current_loc_in_line + 1], int)):
                    self.current_loc_in_line += 1
                    exp += self.current_line[self.current_loc_in_line]
                self.current_token = exp
                self.current_type = TokensMapping.token_type[2]
                exp = ""

            elif (exp == "\""):
                while (self.current_line[self.current_loc_in_line + 1] != "\""):
                    self.current_loc_in_line += 1
                    exp += self.current_line[self.current_loc_in_line]
                self.current_loc_in_line += 1
                self.current_token = exp
                self.current_type = TokensMapping.token_type[3]
                exp = ""

            else:
                if (self.current_line[self.current_loc_in_line + 1] in [" ", "\n"]): # not anyone of the above so an identifier
                    self.current_token = exp
                    self.current_type = TokensMapping.token_type[4] 
                    exp = ""
                            
    
    # returns a clean line from a given Jack line
    # returns None if no valid code
    def clean_line(line):
        if "//" in line:
            line = line[:line.index("//")]
        line = line.strip()  # cleaning any additional white space
        return line

    if __name__ == "__main__":
        main()