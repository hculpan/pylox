import re

from pylox.scanner.TokenType import TokenType
from pylox.scanner.Token import Token
from pylox.exceptions.ScannerExceptions import ScannerException

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
            if token.type == TokenType.STRING:
                tokens.append(token)
                currIdx += 2
            elif token.type != TokenType.WHITESPACE:
                tokens.append(token)
            currIdx += len(token.text)
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
        return Token(token, line[currIdx], currIdx, lineNo)
    else:
        c1 = line[currIdx]
        if currIdx >= len(line) - 1:
            c2 = None
        else:
            c2 = line[currIdx + 1]
        if c1 == '"':
            try:
                found = re.search('^"(.*?)"', line[currIdx:]).group(1)
                return Token(TokenType.STRING, found, currIdx + 1, lineNo)
            except AttributeError:
                raise ScannerException("No closing quote", lineNo)
        elif c1.isalpha() or c1 == "_":
            found = re.search("(^[a-zA-Z][a-zA-Z0-9_]*)", line[currIdx:]).group(1)
            return Token(checkIfKeywordType(found), str(found), currIdx, lineNo)
        elif c1.isdigit():
            found = re.search("(^[+ -]?[0-9]+([.][0-9]*)?)", line[currIdx:]).group(1)
            return Token(TokenType.NUMBER, str(found), currIdx, lineNo)
        elif c1 == '!':
            if c2 == "=":
                return Token(TokenType.BANG_EQUAL, line[currIdx:currIdx + 2], currIdx, lineNo)
            else:
                return Token(TokenType.BANG, line[currIdx], currIdx, lineNo)
        elif c1 == '=':
            if c2 == '=':
                return Token(TokenType.EQUAL_EQUAL, line[currIdx:currIdx + 2], currIdx, lineNo)
            else:
                return Token(TokenType.EQUAL, line[currIdx], currIdx, lineNo)
        elif c1 == '<':
            if c2 == '=':
                return Token(TokenType.LESS_EQUAL, line[currIdx:currIdx + 2], currIdx, lineNo)
            else:
                return Token(TokenType.LESS, line[currIdx], currIdx, lineNo)
        elif c1 == '>':
            if c2 == '=':
                return Token(TokenType.GREATER_EQUAL, line[currIdx:currIdx + 2], currIdx, lineNo)
            else:
                return Token(TokenType.GREATER, line[currIdx], currIdx, lineNo)
        elif c1 == '|':
            if c2 == '|':
                return Token(TokenType.OR, line[currIdx:currIdx + 2], currIdx, lineNo)
            else:
                raise ScannerException("Unrecognized operator '|' in line {0}".format(lineNo))
        elif c1 == '&':
            if c2 == '&':
                return Token(TokenType.AND, line[currIdx:currIdx + 2], currIdx, lineNo)
            else:
                raise ScannerException("Unrecognized operator '|' in line {0}".format(lineNo))
        elif c1 == '/':
            if c2 == '/':
                eol = line[currIdx:].find('\n')
                if eol == -1:
                    currIdx = len(line)
                else:
                    currIdx = currIdx + eol
            else:
                return Token(TokenType.SLASH, line[currIdx], currIdx, lineNo)


def checkIfKeywordType(text):
    switcher = {
        "class"     : TokenType.CLASS,
        "else"      : TokenType.ELSE,
        "false"     : TokenType.FALSE,
        "fun"       : TokenType.FUN,
        "for"       : TokenType.FOR,
        "if"        : TokenType.IF,
        "nil"       : TokenType.NIL,
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
