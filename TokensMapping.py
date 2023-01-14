class TokensMapping:
    token_type = {
        0: "SYMBOL",
        1: "KEYWORD",
        2: "INTCONST",
        3: "STRING",
        4: "IDENTIFIER"
    }
    
    symbols = {
        "[": 1,
        "]": 2,
        "{": 3,
        "}": 4,
        "(": 5,
        ")": 6,
        "\\": 7,
        ".": 8,
        ",": 9,
        ";": 10,
        "+": 11,
        "-": 12,
        "*": 13,
        "/": 14,
        "&": 15,
        "|": 16,
        "<": 17,
        ">": 18,
        "=": 19,
        "~": 20
    }

    keywords = {
        "class": 1,
        "constructor": 2,
        "function": 3,
        "method": 4,
        "field": 5,
        "static": 6,
        "var": 7,
        "int": 8,
        "char" : 9,
        "boolean": 10,
        "void": 11,
        "true": 12,
        "false": 13,
        "null": 14,
        "this": 15,
        "let": 16,
        "do": 17,
        "if": 18,
        "else": 19,
        "while": 20,
        "return": 21
    }