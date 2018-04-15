from pylox.exceptions.RuntimeException import RuntimeException
from pylox.interpreter.Data import DataType, Data


class Environment:
    def __init__(self, container=None):
        self.container = container
        self.environment = {}

    def declare(self, key):
        self.environment[key] = None, DataType.NIL

    def set(self, key, data):
        if key in self.environment:
            self.environment[key] = data
            return True
        elif self.container is not None and self.container.set(key, data):
            return True
        else:
            raise RuntimeException("Cannot set undefined variable '{0}'".format(key))

    def get(self, key):
        if key in self.environment:
            return self.environment[key]
        elif self.container is not None:
            return self.container.get(key)
        else:
            raise RuntimeException("Undefined variable '{0}'".format(key))
