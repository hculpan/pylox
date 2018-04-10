from enum import Enum


class ExprType(Enum):
    EXPRESSION = 1
    LITERAL = 2
    GROUPING = 3
    UNARY = 4
    BINARY = 5


class DataType(Enum):
    UNKNOWN = 1
    INTEGER = 2
    DOUBLE = 3
    STRING = 4
    BOOLEAN = 5
    NIL = 6


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

    def __repr__(self):
        if self.token is not None:
            return " ({0}[{1}] {2}:{3}) ".format(self.type.name, self.token[1], self.left, self.right)
        else:
            return " ({0} {1}:{2}) ".format(self.type.name, self.left, self.right)

    def evaluate(self):
        return self.eval(self)



