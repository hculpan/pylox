import sys
from pathlib import Path

from pylox.run import runLine
from pylox.error_reporting import clearError
from pylox.EvaluationException import EvaluationException


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
                printResult(result[0], result[1])
            except EvaluationException as err:
                if err.expr.token[3] > 0:
                    print("ERROR: {0}".format(err.message))
                else:
                    print("ERROR: {0} [Line {1}]".format(err.message, err.expr.token[3]))


def printResult(value, dataType):
    print("{0} [{1}]".format(value, dataType))


def runFile(file):
    clearError()
    file = open(file, "r")
    for idx, line in enumerate(file):
        runLine(idx + 1, line)
