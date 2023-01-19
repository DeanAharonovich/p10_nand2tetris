class TokensMapping:
    symbols = {
        "[", "]", "{", "}", "(", ")", "\\", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"}
    keywords = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean",
                "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"
                }
    op_list = {
        "+", "-", "*", "/", "&", "|", "<", ">", "="
    }

#comment
class TokenTypes:
    SYMBOL = "SYMBOL"
    KEYWORD = "KEYWORD"
    INT = "INTCONST"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"


xml_escaping = {
    "<" : "&lt;",
    ">" : "&gt;",
    '"' : "&qout;",
    "&" : "&amp;",
}