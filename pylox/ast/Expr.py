from enum import Enum


class ExprType(Enum):
    EXPRESSION = 1
    LITERAL = 2
    GROUPING = 3
    UNARY = 4


class Expr:
    def __init__(self, exprType=ExprType.EXPRESSION, exprToken=None):
        self.right = None
        self.type = exprType
        self.token = exprToken

    def __repr__(self):
        if self.token is not None:
            return "{0}[{1}]".format(self.type.name, self.token[1])
        else:
            return self.type.name