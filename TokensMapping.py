class TokensMapping:
    symbols = {
        "[", "]", "{", "}", "(", ")", "\\", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"}
    keywords = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean",
                "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"
                }

#comment
class TokenTypes:
    SYMBOL = "SYMBOL"
    KEYWORD = "KEYWORD"
    INT = "INTCONST"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
