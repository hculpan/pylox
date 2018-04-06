from enum import Enum

TokenType = Enum('TokenType',
"""
        LEFT_PAREN RIGHT_PAREN LEFT_BRACE RIGHT_BRACE COMMA DOT MINUS PLUS SEMICOLON SLASH STAR
        BANG BANG_EQUAL EQUAL EQUAL_EQUAL GREATER GREATER_EQUAL LESS LESS_EQUAL
        IDENTIFIER STRING NUMBER
        AND CLASS ELSE FALSE FUN FOR IF NIL OR
        PRINT RETURN SUPER THIS TRUE VAR WHILE
        EOF
""", module=__name__)


def tokenize(line):
    line = list(line.strip())
    tokens = list()
    currToken = ""
    currIdx = 0

    while True:
        token = getNextToken(line, currIdx)
        if token is not None:
            tokens.append(token)
            currIdx += len(token[1])
        else:
            currIdx += 1

        if currIdx >= len(line):
            if currToken != "":
                tokens.append((TokenType.STRING, currToken, currIdx - len(currToken)))
            break

    # currToken = ''
    # for c in line:
    #     if c.isspace():
    #         if currToken != "":
    #             tokens.append(currToken)
    #         currToken = ""
    #     elif c == "\"" or c == "." or c == "!" or c == ";":
    #         if currToken != "":
    #             tokens.append(currToken)
    #         tokens.append(c)
    #         currToken = ""
    #     else:
    #         currToken += c
    #
    # if currToken != "":
    #     tokens.append(currToken)

    return tokens


def getNextToken(line, currIdx):
    switcher = {
        '(': TokenType.LEFT_PAREN,
        ')': TokenType.RIGHT_PAREN,
        '{': TokenType.LEFT_BRACE,
        '}': TokenType.RIGHT_BRACE,
        ',': TokenType.COMMA,
        '.': TokenType.DOT,
        '-': TokenType.MINUS,
        '+': TokenType.PLUS,
        ';': TokenType.SEMICOLON,
        '/': TokenType.SLASH,
        '*': TokenType.STAR
    }
    token = switcher.get(line[currIdx])
    if token is not None:
        return token, line[currIdx], currIdx
    else:
        return None
