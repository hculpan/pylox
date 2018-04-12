import re

from pylox.error_reporting import error
from pylox.lexer.TokenType import TokenType

lineNo = 1
currIdx = 0


def tokenize(line):
    global lineNo, currIdx

    line = line.strip()
    tokens = list()
    lineNo = 1
    currIdx = 0

    while True:
        token = getNextToken(line)
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


def getNextToken(line):
    global lineNo, currIdx

    if line[currIdx] == '\n':
        lineNo += 1
        return
    elif line[currIdx] == '\r':
        return

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
        return token, line[currIdx], currIdx, lineNo
    else:
        c1 = line[currIdx]
        if currIdx >= len(line) - 1:
            c2 = None
        else:
            c2 = line[currIdx + 1]
        if c1 == '"':
            try:
                found = re.search('^"(.*?)"', line[currIdx:]).group(1)
                return TokenType.STRING, found, currIdx + 1, lineNo
            except AttributeError:
                error("No closing quote", lineNo)
        elif c1.isalpha() or c1 == "_":
            found = re.search("(^[a-zA-Z][a-zA-Z0-9_]*)", line[currIdx:]).group(1)
            return checkIfKeywordType(found), str(found), currIdx, lineNo
        elif c1.isdigit():
            found = re.search("(^[+ -]?[0-9]+([.][0-9]*)?)", line[currIdx:]).group(1)
            return TokenType.NUMBER, str(found), currIdx, lineNo
        elif c1 == '!':
            if c2 == "=":
                return TokenType.BANG_EQUAL, line[currIdx:currIdx + 2], currIdx, lineNo
            else:
                return TokenType.BANG, line[currIdx], currIdx, lineNo
        elif c1 == '=':
            if c2 == '=':
                return TokenType.EQUAL_EQUAL, line[currIdx:currIdx + 2], currIdx, lineNo
            else:
                return TokenType.EQUAL, line[currIdx], currIdx, lineNo
        elif c1 == '<':
            if c2 == '=':
                return TokenType.LESS_EQUAL, line[currIdx:currIdx + 2], currIdx, lineNo
            else:
                return TokenType.LESS, line[currIdx], currIdx, lineNo
        elif c1 == '>':
            if c2 == '=':
                return TokenType.GREATER_EQUAL, line[currIdx:currIdx + 2], currIdx, lineNo
            else:
                return TokenType.GREATER, line[currIdx], currIdx, lineNo
        elif c1 == '/':
            if c2 == '/':
                eol = line[currIdx:].find('\n')
                if eol == -1:
                    currIdx = len(line)
                else:
                    currIdx = currIdx + eol
            else:
                return TokenType.SLASH, line[currIdx], currIdx, lineNo


def checkIfKeywordType(text):
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
    if value is None:
        value = TokenType.IDENTIFIER
    return value