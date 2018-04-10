from pylox.lexer.scanner import tokenize
from pylox.parser.parser import parse


def runLine(lineNo, line):
    tokens = tokenize(line, lineNo)
    ast = parse(tokens)
    # print("{0}".format(ast))
    print("{0}".format(ast.eval(ast)))

