from pylox.ast.Expr import Expr, ExprType
from pylox.lexer.scanner import TokenType
from pylox.error_reporting import error

currIdx = 0
tokens = list()


def parse(tokenList):
    global tokens, currIdx
    currIdx = 0
    tokens = tokenList
    return expression()


def expression():
    expr = Expr()
    currExpr = expr
    while not isEndOfTokens():
        currExpr.right = unary()
        currExpr = currExpr.right

        # Temporary kludge
        if matchesToken(TokenType.RIGHT_PAREN):
            break

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
    if matchesToken(TokenType.FALSE, TokenType.TRUE, TokenType.NIL, TokenType.NUMBER, TokenType.STRING):
        result.type = ExprType.LITERAL
        result.token = nextToken()
    elif matchesToken(TokenType.LEFT_PAREN):
        result.type = ExprType.GROUPING
        result.token = nextToken()
        result.right = expression()
        if not matchesToken(TokenType.RIGHT_PAREN):
            error("Expecting ')', found {0}".format(peekToken()[1]), peekToken()[3])
        else:
            nextToken()
#    elif matchesToken(TokenType.RIGHT_PAREN):
#        error("Found unmatched ')'", peekToken()[3])
#        nextToken()

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
