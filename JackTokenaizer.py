from TokensMapping import TokensMapping, TokenTypes


class JackTokenaizer:
    def __init__(self, inputFile):
        self.current_token = None
        self.current_type = None
        self.in_file = open(inputFile, "r")
        self.current_loc_in_line = 0

    def advance(self):

        buffer = ""
        self.current_token = None

        while self.current_token is None:
            buffer += self.in_file.read(1)
            if buffer in {" ", "\n"}:
                buffer = ""

            if "//" in buffer:
                while not buffer.endswith('\n'):
                    buffer += self.in_file.read(1)
                buffer = ""

            if "/**" in buffer:
                while not buffer.endswith('*/'):
                    buffer += self.in_file.read(1)
                buffer = buffer[:buffer.index("/**")] 

            if buffer in TokensMapping.symbols:
                if buffer == "/":
                    if self.in_file.read(1) in ("/", "*"):
                        self.in_file.seek(self.in_file.tell()-1)
                        continue
                self.current_token = buffer
                self.current_type = TokenTypes.SYMBOL

            if buffer in TokensMapping.keywords:
                self.current_token = buffer
                self.current_type = TokenTypes.KEYWORD

            if buffer.startswith('"'):
                while not buffer.endswith('"'):
                    buffer += self.in_file.read(1)
                self.current_token = buffer[1:-1]
                self.current_type = TokenTypes.STRING

            if buffer.isdigit():
                while buffer.isdigit():
                    buffer += self.in_file.read(1)

                self.current_token = buffer[:-1]
                self.in_file.seek(self.in_file.tell() - 1)
                self.current_type = TokenTypes.INT

            if buffer and buffer[-1] in {" ", "\n"}:  # not anyone of the above so an identifier
                self.current_token = buffer[-1]
                self.current_type = TokenTypes.IDENTIFIER

    # returns a clean line from a given Jack line
    # returns None if no valid code
    def clean_line(line):
        if "//" in line:
            line = line[:line.index("//")]
        line = line.strip()  # cleaning any additional white space
        return line


if __name__ == "__main__":
    JackTokenaizer("./text.txt").advance()
