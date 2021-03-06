from enum import Enum

from pylox.interpreter.Data import DataType


class ExprType(Enum):
    EXPRESSION = 1
    LITERAL = 2
    GROUPING = 3
    UNARY = 4
    BINARY = 5
    PRINT = 6
    VAR = 7
    IDENTIFIER = 8
    ASSIGNMENT = 9
    BLOCK = 10
    IF = 11
    OR = 12
    AND = 13
    WHILE = 14
    FOR = 15
    CALL = 16
    ARGUMENTS = 17
    FUNCTION = 18
    RETURN = 19


def defaultEval(self):
    return None, DataType.UNKNOWN


class Expr:
    def __init__(self, exprType=ExprType.EXPRESSION, exprToken=None):
        self.right = None
        self.left = None
        self.type = exprType
        self.token = exprToken
        self.eval = defaultEval
        self.value = None
        self.dataType = DataType.UNKNOWN
        self.condition = None
        self.increment = None

    def __repr__(self):
        if self.token is not None:
            return " ({0}[{1}] {2}:{3}) ".format(self.type.name, self.token[1], self.left, self.right)
        else:
            return " ({0} {1}:{2}) ".format(self.type.name, self.left, self.right)

    def evaluate(self):
        return self.eval(self)



