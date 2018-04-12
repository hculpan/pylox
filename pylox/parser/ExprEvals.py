from pylox.error_reporting import error
from pylox.lexer.TokenType import TokenType
from pylox.ast.Expr import DataType
from pylox.EvaluationException import EvaluationException


environment = {}


def evalVariableGet(self):
    return environment[self.token[1]]


def evalVariableSet(self):
    environment[self.token[1]] = self.right.right.evaluate()


def evalVariableDecl(self):
    if self.right is None:
        raise EvaluationException("No right node on var declaration", self)
    environment[self.right.token[1]] = None, DataType.NIL
    if self.right.right is not None and self.right.right.token[0] == TokenType.EQUAL:
        evalVariableSet(self.right)


def evalExpr(self):
    if self.left is not None:
        EvaluationException("Left on EXPRESSION is not none!  What do I do?", self)
    if self.right is not None:
        return self.right.evaluate()


def evalLiteral(self):
    return self.value, self.dataType


def evalGrouping(self):
    return self.right.evaluate()


def evalUnary(self):
    if self.right is None:
        error("No right node for unary operator")

    v = self.right.evaluate()
    if self.token[0] == TokenType.MINUS and isNumberType(v[1]):
        return v[0] * -1, v[1]
    else:
        raise EvaluationException("Invalid data type for unary operator", self.right)


def evalPrint(self):
    if self.right is None:
        raise EvaluationException("Invalid statement, missing expression", self)

    m1 = self.right.evaluate()
    if m1[1] == DataType.BOOLEAN and m1[0]:
        print("true")
    elif m1[1] == DataType.BOOLEAN and not m1[0]:
        print("false")
    elif m1[1] == DataType.NIL:
        print("nil")
    else:
        print(m1[0])


def evalMultiplication(self):
    if self.left is None:
        raise EvaluationException("Left mode missing", self)
    elif self.right is None:
        raise EvaluationException("Right mode missing", self)

    m1 = self.left.evaluate()
    if m1[1] != DataType.INTEGER and m1[1] != DataType.DOUBLE:
        raise EvaluationException("Invalid data type for operation", self.left)
    m2 = self.right.evaluate()
    if m2[1] != DataType.INTEGER and m2[1] != DataType.DOUBLE:
        raise EvaluationException("Invalid data type for operation", self.right)

    if self.token[0] == TokenType.STAR and m1[1] == DataType.INTEGER and m2[1] == DataType.INTEGER:
        return m1[0] * m2[0], DataType.INTEGER
    elif self.token[0] == TokenType.STAR:
        return float(m1[0] * m2[0]), DataType.DOUBLE
    elif self.token[0] == TokenType.SLASH:
        return m1[0] / m2[0], DataType.DOUBLE


def isNumberType(dataType):
    return dataType == DataType.INTEGER or dataType == DataType.DOUBLE


def evalEquality(self):
    if self.left is None:
        raise EvaluationException("Left mode missing", self)
    elif self.right is None:
        raise EvaluationException("Left mode missing", self)

    m1 = self.left.evaluate()
    m2 = self.right.evaluate()

    if m1[1] == DataType.NIL or m2[1] == DataType.NIL:
        return False, DataType.BOOLEAN

    if ((m1[1] == DataType.STRING and m2[1] == DataType.STRING) or
            (m1[1] == DataType.BOOLEAN and m2[1] == DataType.BOOLEAN) or
            (isNumberType(m1[1]) and isNumberType(m2[1]))):
        if self.token[0] == TokenType.EQUAL_EQUAL:
            return m1[0] == m2[0], DataType.BOOLEAN
        if self.token[0] == TokenType.BANG_EQUAL:
            return m1[0] != m2[0], DataType.BOOLEAN
    else:
        raise EvaluationException("Invalid data type for equality", self)


def evalComparison(self):
    if self.left is None:
        raise EvaluationException("Left mode missing", self)
    elif self.right is None:
        raise EvaluationException("Left mode missing", self)

    m1 = self.left.evaluate()
    m2 = self.right.evaluate()

    if m1[1] == DataType.NIL or m2[1] == DataType.NIL:
        return False, DataType.BOOLEAN

    if ((m1[1] == DataType.STRING and m2[1] == DataType.STRING) or
        (m1[1] == DataType.BOOLEAN and m2[1] == DataType.BOOLEAN) or
        (isNumberType(m1[1]) and isNumberType(m2[1]))):
        if self.token[0] == TokenType.GREATER:
            return m1[0] > m2[0], DataType.BOOLEAN
        if self.token[0] == TokenType.GREATER_EQUAL:
            return m1[0] >= m2[0], DataType.BOOLEAN
        if self.token[0] == TokenType.LESS:
            return m1[0] < m2[0], DataType.BOOLEAN
        if self.token[0] == TokenType.LESS_EQUAL:
            return m1[0] <= m2[0], DataType.BOOLEAN
    else:
        raise EvaluationException("Invalid data type for comparison", self)


def evalAddition(self):
    if self.left is None:
        raise EvaluationException("Left mode missing", self)
    elif self.right is None:
        raise EvaluationException("Left mode missing", self)

    m1 = self.left.evaluate()
    if not isNumberType(m1[1]) and m1[1] != DataType.STRING:
        raise EvaluationException("Invalid data type for operation", self.left)
    m2 = self.right.evaluate()
    if not isNumberType(m2[1]) and m2[1] != DataType.STRING:
        raise EvaluationException("Invalid data type for operation", self.right)

    if self.token[0] == TokenType.PLUS and m1[1] == DataType.INTEGER and m2[1] == DataType.INTEGER:
        return m1[0] + m2[0], DataType.INTEGER
    elif self.token[0] == TokenType.PLUS and isNumberType(m1[1]) and isNumberType(m2[1]):
        return float(m1[0] + m2[0]), DataType.DOUBLE
    elif self.token[0] == TokenType.PLUS and m1[1] == DataType.STRING and isNumberType(m2[1]):
        return m1[0] + str(m2[0]), DataType.STRING
    elif self.token[0] == TokenType.PLUS and isNumberType(m1[1]) and m2[1] == DataType.STRING:
        return str(m1[0]) + m2[0], DataType.STRING
    elif self.token[0] == TokenType.PLUS and m1[1] == DataType.STRING and m2[1] == DataType.STRING:
        return m1[0] + m2[0], DataType.STRING
    elif self.token[0] == TokenType.MINUS and m1[1] == DataType.INTEGER and m2[1] == DataType.INTEGER:
        return m1[0] - m2[0], DataType.INTEGER
    elif self.token[0] == TokenType.MINUS and isNumberType(m1[1]) and isNumberType(m2[1]):
        return m1[0] - m2[0], DataType.DOUBLE
    else:
        raise EvaluationException("Data type mismatch in addition/subtraction", self)

