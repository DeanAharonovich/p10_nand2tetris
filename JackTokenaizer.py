import re

from CompilationEngine import CompilationEngine

class JackTokenaizer:
    def __init__(self, inputFile, output_file):
        self.current_token = None
        self.current_type = None
        self.symbols = re.compile("[{}()\[\].,;+\-*\/&|<>=~]")
        self.keywords = re.compile("""(class|constructor|function|method|field|static|var|int|char|
                                      boolean|void|true|false|null|this|let|do|if|else|while|return)""")
        self.integerConst = re.compile("\b\d+\b")
        self.string = re.compile("[\"](.*)[\"]")
        self.identifier = re.compile("\b[A-Za-z_][A-Za-z_0-9]*\b")
        self.in_file = inputFile
        self.out_file = output_file

    def main(self):
        with open(self.in_file, "r") as in_file:
            with open(self.out_file, "w") as out_file:
                for line in in_file:
                    self.clean_line(line)
                    if line:
                        exp = ""
                        for char in line:
                            exp += char
                            exp_match = self.symbols.match(exp)
                            if exp_match is not None:
                                xml = self.write_xml(exp_match, "sym")
                                out_file.write(xml)
                                exp = ""
                            
                            exp_match = self.keywords.match(exp)
                            if exp_match is not None:
                                xml = self.write_xml(exp_match, "key")
                                out_file.write(xml)
                                exp = ""
                            
                            exp_match = self.integerConst.match(exp)
                            if exp_match is not None:
                                xml = self.write_xml(exp_match, "int")
                                out_file.write(xml)
                                exp = ""

                            exp_match = self.string.match(exp)
                            if exp_match is not None:
                                xml = self.write_xml(exp_match, "str")
                                out_file.write(xml)
                                exp = ""

                            exp_match = self.identifier.match(exp)
                            if exp_match is not None:
                                xml = CompilationEngine.write_xml(exp_match, "ide")
                                out_file.write(xml)
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