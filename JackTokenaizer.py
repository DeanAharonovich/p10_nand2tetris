from TokensMapping import TokensMapping, TokenTypes


class JackTokenaizer:
    def __init__(self, inputFile):
        self.current_token = None
        self.current_type = None
        self.in_file = open(inputFile, "r")
        self.next_char = self.in_file.read(1)

    def advance(self):
        buffer = ""
        self.current_token = None

        while self.current_token is None:
            current_char = self.next_char
            self.next_char = self.in_file.read(1)

            buffer += current_char

            if buffer == "":
                return

            if buffer in {" ", "\n", "\t"}:
                buffer = ""

            if "//" in buffer:
                while not buffer.endswith('\n'):
                    buffer += self.next_char
                    self.next_char = self.in_file.read(1)
                buffer = ""

            if "/*" in buffer:
                while not buffer.endswith('*/'):
                    buffer += self.next_char
                    self.next_char = self.in_file.read(1)
                buffer = buffer[:buffer.index("/**")]

            if buffer in TokensMapping.symbols:
                if buffer == "/":

                    if self.next_char in ("/", "*"):
                        buffer += self.next_char
                        self.next_char = self.in_file.read(1)
                        continue
                self.current_token = buffer
                self.current_type = TokenTypes.SYMBOL
                break

            if buffer in TokensMapping.keywords:
                if self.next_char.isalpha():
                    continue
                self.current_token = buffer
                self.current_type = TokenTypes.KEYWORD
                break

            if buffer.startswith('"'):
                while not self.next_char == '"':
                    buffer += self.next_char
                    self.next_char = self.in_file.read(1)
                buffer += self.next_char
                self.next_char = self.in_file.read(1)
                self.current_token = buffer[1:-1]
                self.current_type = TokenTypes.STRING
                break

            if buffer.isdigit():
                while self.next_char.isdigit():
                    buffer += self.next_char
                    self.next_char = self.in_file.read(1)

                self.current_token = buffer
                self.current_type = TokenTypes.INT
                break

            # not anyone of the above so an identifier
            if len(buffer) > 0 and not (self.next_char.isdigit() or self.next_char.isalpha() or self.next_char == "_"):
                self.current_token = buffer
                self.current_type = TokenTypes.IDENTIFIER
                break

    def nextChar(self):
        return self.next_char

