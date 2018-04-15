class RuntimeException(Exception):
    def __init__(self, message, expr=None):
        self.message = message
        self.expr = expr