from pylox.error_reporting import error
from pylox.scanner.TokenType import TokenType
from pylox.ast.Expr import ExprType
from pylox.interpreter.Environment import Environment
from pylox.interpreter.Functions import *
from pylox.exceptions.RuntimeException import RuntimeException
from pylox.exceptions.Return import Return


environment = Environment()
currentBlockEnvironment = environment


def initEnvironment():
    environment.declare('clock')
    environment.set('clock', ClockFunction())
    environment.declare('mod')
    environment.set('mod', ModFunction())


def getCurrentBlockEnvironment():
    global currentBlockEnvironment
    return currentBlockEnvironment


def evalFunc(self):
    global currentBlockEnvironment

    closure = Environment(currentBlockEnvironment)
    func = Function(self.value, self.left, self.right, closure)

    currentBlockEnvironment.declare(self.value)
    currentBlockEnvironment.set(self.value, func)


def confirmArityMatch(func, args):
    if (args is None and len(func.params) > 0) or (args is not None and len(args) != len(func.params)):
        raise RuntimeException('For call to "{0}": expected {1} arguments, found {2}'.format(func.value, len(func.params), len(args)))


def evalReturn(self):
    if self.right is not None:
        raise Return(self.right.evaluate())
    else:
        raise Return(Data(None, DataType.NIL))


def evalCall(self):
    global currentBlockEnvironment

    func = currentBlockEnvironment.get(self.left.token.text)
    if func is not None:
        args = self.right
        confirmArityMatch(func, args)
        arguments = list()
        if args is not None and len(args) > 0:
            for arg in args:
                arguments.append(arg.evaluate())

        tmpCurrentBlockEnvironment = currentBlockEnvironment
        try:

            if func.closure is None:
                currentBlockEnvironment = Environment(currentBlockEnvironment)
            else:
                currentBlockEnvironment = Environment(func.closure)

            if func.params is not None and len(func.params) > 0:
                for idx in range(len(func.params)):
                    param = func.params[idx]
                    v = arguments[idx]
                    currentBlockEnvironment.declare(param.text)
                    currentBlockEnvironment.set(param.text, v)

            if hasattr(func, 'call'):
                result = func.call(currentBlockEnvironment)
            else:
                result = func.block.evaluate()
        except Return as r:
            result = r.value
        finally:
            currentBlockEnvironment = tmpCurrentBlockEnvironment
        return result


def evalFor(self):
    global currentBlockEnvironment

    tmpCurrentBlockEnvironment = currentBlockEnvironment
    try:
        currentBlockEnvironment = Environment(currentBlockEnvironment)
        if self.left is not None:
            self.left.evaluate()

        while isTrue(self.condition.evaluate()):
            self.right.evaluate()
            if self.increment is not None:
                self.increment.evaluate()
    finally:
        currentBlockEnvironment = tmpCurrentBlockEnvironment


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
        raise RuntimeException("No conditional given", self)
    b = isTrue(self.condition.evaluate())
    if b and self.left is not None:
        self.left.evaluate()
    elif not b and self.right is not None:
        self.right.evaluate()


def isTrue(data):
    if data.type == DataType.BOOLEAN:
        return data.value
    elif data.type == DataType.STRING:
        return data.value != ""
    elif isNumberType(data.type):
        return data.value > 0
    else:
        return False


def evalBlock(self):
    global currentBlockEnvironment

    tmpCurrentBlock = currentBlockEnvironment
    try:
        currentBlockEnvironment = Environment(currentBlockEnvironment)
        for statement in self.right:
            statement.evaluate()
    finally:
        currentBlockEnvironment = tmpCurrentBlock


def evalVariableGet(self):
    global currentBlockEnvironment

    return currentBlockEnvironment.get(self.token.text)


def evalVariableDecl(self):
    global currentBlockEnvironment

    if self.left is None:
        raise RuntimeException("No left node on var declaration", self)
    if self.right is not None:
        data = self.right.evaluate()
        currentBlockEnvironment.declare(self.left.token.text)
        currentBlockEnvironment.set(self.left.token.text, data)
    else:
        currentBlockEnvironment.declare(self.left.token.text)


def evalAssignment(self):
    global currentBlockEnvironment

    if self.right is None:
        raise RuntimeException('No r-value for assignment', self)
    if self.left is None:
        raise RuntimeException('No l-value for assignment', self)
    data = self.right.evaluate()
    currentBlockEnvironment.set(self.left.token.text, data)
    return data


def evalExpr(self):
    if self.left is not None:
        RuntimeException("Left on EXPRESSION is not none!  What do I do?", self)
    if self.right is not None:
        return self.right.evaluate()


def evalLiteral(self):
    return Data(self.value, self.dataType)


def evalGrouping(self):
    return self.right.evaluate()


def evalUnary(self):
    if self.right is None:
        error("No right node for unary operator")

    v = self.right.evaluate()
    if self.token.type == TokenType.MINUS and isNumberType(v.type):
        return Data(v.value * -1, v.type)
    elif self.token.type == TokenType.BANG and v.type == DataType.BOOLEAN:
        return Data(not v.value, v.type)
    else:
        raise RuntimeException("Invalid data type for unary operator", self.right)


def evalPrint(self):
    if self.right is None:
        raise RuntimeException("Invalid statement, missing expression", self)

    m1 = self.right.evaluate()
    if m1.type == DataType.BOOLEAN and m1.value:
        print("true")
    elif m1.type == DataType.BOOLEAN and not m1.value:
        print("false")
    elif m1.type == DataType.NIL:
        print("nil")
    else:
        print(m1.value)


def evalMultiplication(self):
    if self.left is None:
        raise RuntimeException("Left mode missing", self)
    elif self.right is None:
        raise RuntimeException("Right mode missing", self)

    m1 = self.left.evaluate()
    if m1.type != DataType.INTEGER and m1.type != DataType.DOUBLE:
        raise RuntimeException("Invalid data type for operation", self.left)
    m2 = self.right.evaluate()
    if m2.type != DataType.INTEGER and m2.type != DataType.DOUBLE:
        raise RuntimeException("Invalid data type for operation", self.right)

    if self.token.type == TokenType.STAR and m1.type == DataType.INTEGER and m2.type == DataType.INTEGER:
        return Data(m1.value * m2.value, DataType.INTEGER)
    elif self.token.type == TokenType.STAR:
        return Data(float(m1.value * m2.value), DataType.DOUBLE)
    elif self.token.type == TokenType.SLASH:
        return Data(m1.value / m2.value, DataType.DOUBLE)


def isNumberType(dataType):
    return dataType == DataType.INTEGER or dataType == DataType.DOUBLE


def evalEquality(self):
    if self.left is None:
        raise RuntimeException("Left mode missing", self)
    elif self.right is None:
        raise RuntimeException("Left mode missing", self)

    m1 = self.left.evaluate()
    m2 = self.right.evaluate()

    if m1.type == DataType.NIL or m2.type == DataType.NIL:
        return Data(False, DataType.BOOLEAN)

    if ((m1.type == DataType.STRING and m2.type == DataType.STRING) or
            (m1.type == DataType.BOOLEAN and m2.type == DataType.BOOLEAN) or
            (isNumberType(m1.type) and isNumberType(m2.type))):
        if self.token.type == TokenType.EQUAL_EQUAL:
            return Data(m1.value == m2.value, DataType.BOOLEAN)
        if self.token.type == TokenType.BANG_EQUAL:
            return Data(m1.value != m2.value, DataType.BOOLEAN)
    else:
        raise RuntimeException("Invalid data type for equality", self)


def evalComparison(self):
    if self.left is None:
        raise RuntimeException("Left mode missing", self)
    elif self.right is None:
        raise RuntimeException("Left mode missing", self)

    m1 = self.left.evaluate()
    m2 = self.right.evaluate()

    if m1.type == DataType.NIL or m2.type == DataType.NIL:
        return Data(False, DataType.BOOLEAN)

    if ((m1.type == DataType.STRING and m2.type == DataType.STRING) or
        (m1.type == DataType.BOOLEAN and m2.type == DataType.BOOLEAN) or
        (isNumberType(m1.type) and isNumberType(m2.type))):
        if self.token.type == TokenType.GREATER:
            return Data(m1.value > m2.value, DataType.BOOLEAN)
        if self.token.type == TokenType.GREATER_EQUAL:
            return Data(m1.value >= m2.value, DataType.BOOLEAN)
        if self.token.type == TokenType.LESS:
            return Data(m1.value < m2.value, DataType.BOOLEAN)
        if self.token.type == TokenType.LESS_EQUAL:
            return Data(m1.value <= m2.value, DataType.BOOLEAN)
    else:
        raise RuntimeException("Invalid data type for comparison", self)


def evalAddition(self):
    if self.left is None:
        raise RuntimeException("Left mode missing", self)
    elif self.right is None:
        raise RuntimeException("Left mode missing", self)

    m1 = self.left.evaluate()
    if not isNumberType(m1.type) and m1.type != DataType.STRING:
        raise RuntimeException("Invalid data type for operation", self.left)
    m2 = self.right.evaluate()
    if not isNumberType(m2.type) and m2.type != DataType.STRING:
        raise RuntimeException("Invalid data type for operation", self.right)

    if self.token.type == TokenType.PLUS and m1.type == DataType.INTEGER and m2.type == DataType.INTEGER:
        return Data(m1.value + m2.value, DataType.INTEGER)
    elif self.token.type == TokenType.PLUS and isNumberType(m1.type) and isNumberType(m2.type):
        return Data(float(m1.value + m2.value), DataType.DOUBLE)
    elif self.token.type == TokenType.PLUS and m1.type == DataType.STRING and isNumberType(m2.type):
        return Data(m1.value + str(m2.value), DataType.STRING)
    elif self.token.type == TokenType.PLUS and isNumberType(m1.type) and m2.type == DataType.STRING:
        return Data(str(m1.value) + m2.value, DataType.STRING)
    elif self.token.type == TokenType.PLUS and m1.type == DataType.STRING and m2.type == DataType.STRING:
        return Data(m1.value + m2.value, DataType.STRING)
    elif self.token.type == TokenType.MINUS and m1.type == DataType.INTEGER and m2.type == DataType.INTEGER:
        return Data(m1.value - m2.value, DataType.INTEGER)
    elif self.token.type == TokenType.MINUS and isNumberType(m1.type) and isNumberType(m2.type):
        return Data(m1.value - m2.value, DataType.DOUBLE)
    else:
        raise RuntimeException("Data type mismatch in addition/subtraction", self)

