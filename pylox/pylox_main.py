import sys
from pathlib import Path

from pylox.run import runLine, runProgram
from pylox.error_reporting import clearError
from pylox.EvaluationException import EvaluationException
from pylox.ParseException import ParseException
from pylox.ast.Expr import DataType


def main():
    if len(sys.argv) == 1:
        runPrompt()
    elif len(sys.argv) == 2:
        file = Path(sys.argv[1])
        if not file.exists():
            print("The specified file, {0}, is not found".format(sys.argv[1]))
            return
        elif not file.is_file():
            print("The specified file, {0}, is not a valid file".format(sys.argv[1]))
            return
        else:
            runFile(sys.argv[1])
            return
    else:
        print("Usage: pylox.sh [script]")
        return


def runPrompt():
    print("PyLox REPL environment")

    while True:
        clearError()
        line = input("> ").strip()

        if line == "quit" or line == "bye" or line == "exit":
            print("PyLox session terminated")
            break
        else:
            try:
                result = runLine(0, line)
                if result is not None:
                    printResult(result[0], result[1])
            except EvaluationException as err:
                if err.expr.token[3] > 0:
                    print("Runtime error: {0}".format(err.message))
                else:
                    print("Runtime error: {0} [Line {1}]".format(err.message, err.expr.token[3]))
            except ParseException as err:
                print("Parse error: {0} [Line {1}]".format(err.message, err.lineNo))


def printResult(value, dataType):
    if dataType == DataType.BOOLEAN and value:
        print("{0} [{1}]".format("true", dataType))
    elif dataType == DataType.BOOLEAN and not value:
        print("{0} [{1}]".format("false", dataType))
    else:
        print("{0} [{1}]".format(value, dataType))


def runFile(file):
    clearError()
    file = open(file, "r")
    runProgram(file.read())
