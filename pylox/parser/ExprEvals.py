from pylox.error_reporting import error
from pylox.scanner.TokenType import TokenType
from pylox.ast.Expr import DataType
from pylox.ast.Expr import ExprType
from pylox.exceptions.EvaluationException import EvaluationException
from pylox.interpreter.Environment import Environment


environment = Environment()
currentBlockEnvironment = environment


def evalFor(self):
    self.left.evaluate()
    while isTrue(self.condition.evaluate()):
        self.right.evaluate()
        self.increment.evaluate()


def evalWhile(self):
    while isTrue(self.condition.evaluate()):
        self.right.evaluate()


def evalLogical(self):
    d = self.left.evaluate()
    b = isTrue(d)
    if self.type == ExprType.OR and b:
        return d
    elif self.type == ExprType.AND and not b:
        return d

    return self.right.evaluate()


def evalIf(self):
    if self.condition is None:
        raise EvaluationException("No conditional given", self)
    b = isTrue(self.condition.evaluate())
    if b and self.left is not None:
        self.left.evaluate()
    elif not b and self.right is not None:
        self.right.evaluate()


def isTrue(data):
    if data[1] == DataType.BOOLEAN:
        return data[0]
    elif data[1] == DataType.STRING:
        return data[0] != ""
    elif isNumberType(data[1]):
        return data[0] > 0
    else:
        return False


def evalBlock(self):
    global currentBlockEnvironment

    currentBlockEnvironment = Environment(currentBlockEnvironment)
    for statement in self.right:
        statement.evaluate()
    currentBlockEnvironment = currentBlockEnvironment.container


def evalVariableGet(self):
    global currentBlockEnvironment

    return currentBlockEnvironment.get(self.token.text)


def evalVariableDecl(self):
    global currentBlockEnvironment

    if self.left is None:
        raise EvaluationException("No left node on var declaration", self)
    if self.right is not None:
        data = self.right.evaluate()
        currentBlockEnvironment.declare(self.left.token.text)
        currentBlockEnvironment.set(self.left.token.text, data[0], data[1])
    else:
        currentBlockEnvironment.declare(self.left.token[1])


def evalAssignment(self):
    global currentBlockEnvironment

    if self.right is None:
        raise EvaluationException('No r-value for assignment', self)
    if self.left is None:
        raise EvaluationException('No l-value for assignment', self)
    data = self.right.evaluate()
    currentBlockEnvironment.set(self.left.token.text, data[0], data[1])


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

    if self.token.type == TokenType.STAR and m1[1] == DataType.INTEGER and m2[1] == DataType.INTEGER:
        return m1[0] * m2[0], DataType.INTEGER
    elif self.token.type == TokenType.STAR:
        return float(m1[0] * m2[0]), DataType.DOUBLE
    elif self.token.type == TokenType.SLASH:
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
        if self.token.type == TokenType.EQUAL_EQUAL:
            return m1[0] == m2[0], DataType.BOOLEAN
        if self.token.type == TokenType.BANG_EQUAL:
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
        if self.token.type == TokenType.GREATER:
            return m1[0] > m2[0], DataType.BOOLEAN
        if self.token.type == TokenType.GREATER_EQUAL:
            return m1[0] >= m2[0], DataType.BOOLEAN
        if self.token.type == TokenType.LESS:
            return m1[0] < m2[0], DataType.BOOLEAN
        if self.token.type == TokenType.LESS_EQUAL:
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

    if self.token.type == TokenType.PLUS and m1[1] == DataType.INTEGER and m2[1] == DataType.INTEGER:
        return m1[0] + m2[0], DataType.INTEGER
    elif self.token.type == TokenType.PLUS and isNumberType(m1[1]) and isNumberType(m2[1]):
        return float(m1[0] + m2[0]), DataType.DOUBLE
    elif self.token.type == TokenType.PLUS and m1[1] == DataType.STRING and isNumberType(m2[1]):
        return m1[0] + str(m2[0]), DataType.STRING
    elif self.token.type == TokenType.PLUS and isNumberType(m1[1]) and m2[1] == DataType.STRING:
        return str(m1[0]) + m2[0], DataType.STRING
    elif self.token.type == TokenType.PLUS and m1[1] == DataType.STRING and m2[1] == DataType.STRING:
        return m1[0] + m2[0], DataType.STRING
    elif self.token.type == TokenType.MINUS and m1[1] == DataType.INTEGER and m2[1] == DataType.INTEGER:
        return m1[0] - m2[0], DataType.INTEGER
    elif self.token.type == TokenType.MINUS and isNumberType(m1[1]) and isNumberType(m2[1]):
        return m1[0] - m2[0], DataType.DOUBLE
    else:
        raise EvaluationException("Data type mismatch in addition/subtraction", self)

