from pylox.ast.Expr import Expr, ExprType
from pylox.lexer.scanner import TokenType
from pylox.parser.ExprEvals import *

currIdx = 0
tokens = list()


def parse(tokenList):
    global tokens, currIdx
    currIdx = 0
    tokens = tokenList
    return expression()


def expression():
    expr = Expr()
    expr.eval = evalExpr
    expr.right = equality()
    return expr


def equality():
    expr = comparison()

    while matchesToken(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
        leftExpr = expr
        expr = Expr(ExprType.BINARY, nextToken())
        expr.left = leftExpr
        expr.right = comparison()

    return expr


def comparison():
    expr = addition()

    while matchesToken(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
        leftExpr = expr
        expr = Expr(ExprType.BINARY, nextToken())
        expr.left = leftExpr
        expr.right = addition()

    return expr


def addition():
    expr = multiplication()

    while matchesToken(TokenType.PLUS, TokenType.MINUS):
        leftExpr = expr
        expr = Expr(ExprType.BINARY, nextToken())
        expr.left = leftExpr
        expr.right = multiplication()

    return expr


def multiplication():
    expr = unary()

    while matchesToken(TokenType.SLASH, TokenType.STAR):
        leftExpr = expr
        expr = Expr(ExprType.BINARY, nextToken())
        expr.left = leftExpr
        expr.right = unary()

    return expr


def unary():
    if matchesToken(TokenType.BANG, TokenType.MINUS):
        expr = Expr(ExprType.UNARY, nextToken())
        expr.right = unary()
        return expr
    else:
        return primary()


def primary():
    result = Expr()
    if matchesToken(TokenType.FALSE, TokenType.TRUE, TokenType.NIL, TokenType.STRING, TokenType.NUMBER):
        result.type = ExprType.LITERAL
        result.token = nextToken()
        result.eval = evalLiteral
    elif matchesToken(TokenType.LEFT_PAREN):
        result.type = ExprType.GROUPING
        result.token = nextToken()
        result.right = addition()
        if not matchesToken(TokenType.RIGHT_PAREN):
            error("Expecting ')', found {0}".format(peekToken()[1]), peekToken()[3])
        else:
            nextToken()

    return result


def peekToken():
    return tokens[currIdx]


def nextToken():
    global currIdx
    if isEndOfTokens():
        return None
    else:
        result = tokens[currIdx]
        currIdx += 1
        return result


def prevToken():
    global currIdx
    if currIdx == 0:
        return
    currIdx -= 1


def matchesToken(*tokenTypess):
    currToken = peekToken()
    for tokenType in tokenTypess:
        if tokenType == currToken[0]:
            return True
    return False


def isEndOfTokens():
    return matchesToken(TokenType.EOL)
