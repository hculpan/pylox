from .scanner import tokenize, TokenType
from .error_reporting import error


def runLine(lineNo, line):
    tokens = tokenize(line)

    if lineNo > 0:
        print("Line {0}".format(lineNo))
    for token in tokens:
        if token == "error":
            error("Here's your error!", lineNo)
        print("Token: {0}".format(token))

