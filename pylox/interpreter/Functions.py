import time

from pylox.interpreter.Data import DataType, Data
from pylox.exceptions.RuntimeException import RuntimeException
from pylox.scanner.TokenType import TokenType
from pylox.scanner.Token import Token


class Function(Data):
    def __init__(self, value, params, block, closure):
        self.value = value
        self.type = DataType.FUNCTION
        self.params = params
        self.block = block
        self.closure = closure


class NativeFunction(Function):
    def call(self, env):
        pass


class ClockFunction(NativeFunction):
    def __init__(self):
        self.value = 'clock'
        self.type = DataType.FUNCTION
        self.params = list()
        self.closure = None

    def call(self, env):
        return Data(time.time(), DataType.DOUBLE)


class ModFunction(NativeFunction):
    def __init__(self):
        self.value = 'mod'
        self.type = DataType.FUNCTION
        self.params = [Token(TokenType.IDENTIFIER, "a", 0, 0),
                       Token(TokenType.IDENTIFIER, "b", 0, 0)]
        self.closure = None

    def call(self, env):
        aData = env.get("a")
        if aData is None:
            raise RuntimeException("'a' parameter is not defined in call to mod")
        bData = env.get("b")
        if bData is None:
            raise RuntimeException("'b' parameter is not defined in call to mod")

        if aData.type != DataType.DOUBLE and aData.type != DataType.INTEGER:
            raise RuntimeException("'a' argument for call to mod of invalid type")
        if bData.type != DataType.DOUBLE and bData.type != DataType.INTEGER:
            raise RuntimeException("'b' argument for call to mod of invalid type")

        if aData.type == DataType.INTEGER and bData.type == DataType.INTEGER:
            return Data(aData.value % bData.value, DataType.INTEGER)
        else:
            return Data(aData.value % bData.value, DataType.DOUBLE)
