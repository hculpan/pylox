class EvaluationException(Exception):
    def __init__(self, message, expr):
        self.message = message
        self.expr = expr