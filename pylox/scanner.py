import re

from enum import Enum
from .error_reporting import error

TokenType = Enum('TokenType',
"""
        LEFT_PAREN RIGHT_PAREN LEFT_BRACE RIGHT_BRACE COMMA DOT MINUS PLUS SEMICOLON SLASH STAR
        BANG BANG_EQUAL EQUAL EQUAL_EQUAL GREATER GREATER_EQUAL LESS LESS_EQUAL
        IDENTIFIER STRING NUMBER COMMENT
        AND CLASS ELSE FALSE FUN FOR IF NIL OR
        PRINT RETURN SUPER THIS TRUE VAR WHILE
        EOF WHITESPACE EOL
""", module=__name__)


def tokenize(line, lineNo=0):
    line = line.strip()
    tokens = list()
    currIdx = 0

    while True:
        token = getNextToken(line, currIdx, lineNo)
        if token is not None:
            if token[0] == TokenType.STRING:
                tokens.append(token)
                currIdx += 2
            elif token[0] != TokenType.WHITESPACE:
                tokens.append(token)
            currIdx += len(token[1])
        else:
            currIdx += 1

        if currIdx >= len(line):
            break

    return tokens


def getNextToken(line, currIdx, lineNo):
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
        '*': TokenType.STAR,
        ' ': TokenType.WHITESPACE,
        '\t': TokenType.WHITESPACE
    }
    token = switcher.get(line[currIdx])
    if token is not None:
        return token, line[currIdx], currIdx
    else:
        c1 = line[currIdx]
        if currIdx >= len(line) - 1:
            c2 = None
        else:
            c2 = line[currIdx + 1]
        if c1 == '"':
            try:
                found = re.search('^"(.*?)"', line[currIdx:]).group(1)
                return TokenType.STRING, found, currIdx + 1
            except AttributeError:
                error("No closing quote", lineNo)
        elif c1.isalpha() or c1 == "_":
            found = re.search("(^[a-zA-Z][a-zA-Z0-9_]*)", line[currIdx:]).group(1)
            return checkIfKeywordType(found), str(found), currIdx
        elif c1.isdigit():
            found = re.search("(^[+ -]?[0-9]+([.][0-9]*)?)", line[currIdx:]).group(1)
            return TokenType.NUMBER, str(found), currIdx
        elif c1 == '!':
            if c2 == "=":
                return TokenType.BANG_EQUAL, line[currIdx:currIdx + 2], currIdx
            else:
                return TokenType.BANG, line[currIdx], currIdx
        elif c1 == '=':
            if c2 == '=':
                return TokenType.EQUAL_EQUAL, line[currIdx:currIdx + 2], currIdx
            else:
                return TokenType.EQUAL, line[currIdx], currIdx
        elif c1 == '<':
            if c2 == '=':
                return TokenType.LESS_EQUAL, line[currIdx:currIdx + 2], currIdx
            else:
                return TokenType.LESS, line[currIdx], currIdx
        elif c1 == '>':
            if c2 == '=':
                return TokenType.GREATER_EQUAL, line[currIdx:currIdx + 2], currIdx
            else:
                return TokenType.GREATER, line[currIdx], currIdx
        elif c1 == '/':
            if c2 == '/':
                return TokenType.COMMENT, line[currIdx:], currIdx
            else:
                return TokenType.SLASH, line[currIdx], currIdx


def checkIfKeywordType(text):
#    AND CLASS ELSE FALSE FUN FOR IF NIL OR
#    PRINT RETURN SUPER THIS TRUE VAR WHILE
    switcher = {
        "and"       : TokenType.AND,
        "class"     : TokenType.CLASS,
        "else"      : TokenType.ELSE,
        "false"     : TokenType.FALSE,
        "fun"       : TokenType.FUN,
        "for"       : TokenType.FOR,
        "if"        : TokenType.IF,
        "nil"       : TokenType.NIL,
        "or"        : TokenType.OR,
        "print"     : TokenType.PRINT,
        "return"    : TokenType.RETURN,
        "super"     : TokenType.SUPER,
        "this"      : TokenType.THIS,
        "true"      : TokenType.TRUE,
        "var"       : TokenType.VAR,
        "while"     : TokenType.WHILE
    }
    value = switcher.get(text)
    if value == None:
        value = TokenType.IDENTIFIER
    return value