from pylox.lexer.scanner import tokenize
from .error_reporting import error


def runLine(lineNo, line):
    tokens = tokenize(line, lineNo)

    if lineNo > 0:
        print("Line {0}".format(lineNo))
    for token in tokens:
        if token == "error":
            error("Here's your error!", lineNo)
        print("Token: {0}".format(token))


