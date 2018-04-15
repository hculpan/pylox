from pylox.scanner.scanner import tokenize
from pylox.parser.parser import parse
from pylox.exceptions.ParseException import ParseException
from pylox.exceptions.RuntimeException import RuntimeException
from pylox.interpreter.ExprEvals import initEnvironment


def runLine(lineNo, line):
    tokens = tokenize(line, lineNo)
    statements = parse(tokens)
    if len(statements) == 1:
        return statements[0].evaluate()
    else:
        for statement in statements:
            statement.evaluate()


def runProgram(prog):
    tokens = tokenize(prog)
    try:
        statements = parse(tokens)
        initEnvironment()
        for statement in statements:
            statement.evaluate()
    except ParseException as err:
        if err.token is None:
            print("Parse error: {0}".format(err.message))
        else:
            print("Parse error: {0} [Line {1}]".format(err.message, err.token.lineNo))
    except RuntimeException as err:
        if err.expr is None or err.expr.token is None or err.expr.token.lineNo == 0:
            print("Runtime error: {0}".format(err.message))
        else:
            print("Runtime error: {0} [Line {1}]".format(err.message, err.expr.token.lineNo))




