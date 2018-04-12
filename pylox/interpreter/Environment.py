from pylox.EvaluationException import EvaluationException
from pylox.ast.Expr import DataType


class Environment:
    def __init__(self, container=None):
        self.container = container
        self.environment = {}

    def declare(self, key):
        self.environment[key] = None, DataType.NIL

    def set(self, key, value, dataType):
        if key in self.environment:
            self.environment[key] = value, dataType
            return True
        elif self.container is not None and self.container.set(key, value, dataType):
            return True
        else:
            raise EvaluationException("Cannot set undefined variable '{0}'".format(key))

    def get(self, key):
        if key in self.environment:
            return self.environment[key]
        elif self.container is not None:
            return self.container.get(key)
        else:
            raise EvaluationException("Undefined variable '{0}'".format(key))
