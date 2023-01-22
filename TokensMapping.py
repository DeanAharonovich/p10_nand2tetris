class TokensMapping:
    symbols = {
        "[", "]", "{", "}", "(", ")", "\\", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"}
    keywords = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean",
                "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"
                }
    op_list = {
        "+", "-", "*", "/", "&", "|", "<", ">", "="
    }


# comment
class TokenTypes:
    SYMBOL = "SYMBOL"
    KEYWORD = "KEYWORD"
    INT = "INTCONST"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"


class LabelTypes:
    CLASS = 'class'
    SUBROUTINE_DEC = "subroutineDec"
    PARAMETER_LIST = "parameterList"
    SUBROUTINE_BODY = "subroutineBody"
    STATEMENTS = "statements"
    LET_STATEMENT = "letStatement"
    IF_STATEMENT = "ifStatement"
    WHILES_TATEMENT = "whileStatement"
    DO_STATEMENT = "doStatement"
    RETURN_STATEMENT = "returnStatement"
    EXPRESSION = "expression"
    TERM = "term"
    EXPRESSION_LIST = "expressionList"
    SYMBOL = "symbol"
    KEYWORD = "keyword"
    IDENTIFIER = "identifier"
    STRING_CONSTANT = "stringConstant"
    INTEGER_CONSTANT = "integerConstant"
    CLASS_VAR_DEC ="classVarDec"
    VAR_DEC = "varDec"
