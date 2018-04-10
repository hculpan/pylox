from pylox.error_reporting import error
from pylox.lexer.scanner import TokenType


def evalExpr(self):
    if self.left is not None:
        error("Left on EXPRESSION is not none!  What do I do?")
    if self.right is not None:
        return self.right.eval(self.right)


def evalLiteral(self):
    if self.token[0] == TokenType.STRING:
        return self.token[1]
    elif self.token[0] == TokenType.TRUE:
        return True
    elif self.token[0] == TokenType.FALSE:
        return False
    elif self.token[0] == TokenType.NIL:
        return None
    elif self.token[0] == TokenType.NUMBER:
        return float(self.token[1])


