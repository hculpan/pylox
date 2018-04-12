from pylox.ast.Expr import Expr, ExprType
from pylox.parser.ExprEvals import *
from pylox.ast.Expr import DataType
from pylox.lexer.scanner import TokenType
from pylox.ParseException import ParseException

currIdx = 0
tokens = list()


def parse(tokenList):
    global tokens, currIdx
    currIdx = 0
    tokens = tokenList
    stmts = list()
    while not isEndOfTokens():
        stmts.append(declaration())
    return stmts


def declaration():
    if matchesToken(TokenType.VAR):
        result = varDecl()
    else:
        result = statement()
    consume(TokenType.SEMICOLON)
    return result


def varDecl():
    expr = Expr(ExprType.VAR, nextToken())
    if matchesToken(TokenType.IDENTIFIER):
        expr.left = Expr(ExprType.IDENTIFIER, nextToken())
        expr.eval = evalVariableDecl
    else:
        raise ParseException("Identifier expected, found {0}".format(peekToken()[1]), 0)
    if matchesToken(TokenType.EQUAL):
        nextToken()
        expr.right = expression()

    return expr


def statement():
    if matchesToken(TokenType.PRINT):
        return printStmt()
    elif matchesToken(TokenType.LEFT_BRACE):
        return block()
    else:
        return expression()


def block():
    expr = Expr(ExprType.BLOCK, nextToken())
    expr.eval = evalBlock

    statements = list()
    while not matchesToken(TokenType.RIGHT_BRACE) and not isEndOfTokens():
        statements.append(declaration())

    if matchesToken(TokenType.RIGHT_BRACE):
        nextToken()
    expr.right = statements
    return expr


def printStmt():
    expr = Expr(ExprType.PRINT)
    expr.token = nextToken()
    expr.eval = evalPrint
    expr.right = expression()
    return expr


def expression():
    expr = Expr()
    expr.eval = evalExpr
    return assignment()


def assignment():
    expr = equality()

    if matchesToken(TokenType.EQUAL):
        assExpr = Expr(ExprType.ASSIGNMENT, nextToken())
        assExpr.eval = evalAssignment
        assExpr.left = expr
        assExpr.right = assignment()
        expr = assExpr

    return expr


def equality():
    expr = comparison()

    while matchesToken(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
        leftExpr = expr
        expr = Expr(ExprType.BINARY, nextToken())
        expr.eval = evalEquality
        expr.left = leftExpr
        expr.right = comparison()

    return expr


def comparison():
    expr = addition()

    while matchesToken(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
        leftExpr = expr
        expr = Expr(ExprType.BINARY, nextToken())
        expr.eval = evalComparison
        expr.left = leftExpr
        expr.right = addition()

    return expr


def addition():
    expr = multiplication()

    while matchesToken(TokenType.PLUS, TokenType.MINUS):
        leftExpr = expr
        expr = Expr(ExprType.BINARY, nextToken())
        expr.eval = evalAddition
        expr.left = leftExpr
        expr.right = multiplication()

    return expr


def multiplication():
    expr = unary()

    while matchesToken(TokenType.SLASH, TokenType.STAR):
        leftExpr = expr
        expr = Expr(ExprType.BINARY, nextToken())
        expr.eval = evalMultiplication
        expr.left = leftExpr
        expr.right = unary()

    return expr


def unary():
    if matchesToken(TokenType.BANG, TokenType.MINUS):
        expr = Expr(ExprType.UNARY, nextToken())
        expr.eval = evalUnary
        expr.right = unary()
        return expr
    else:
        return primary()


def primary():
    result = Expr()
    if matchesToken(TokenType.LEFT_PAREN):
        result.type = ExprType.GROUPING
        result.token = nextToken()
        result.right = addition()
        result.eval = evalGrouping
        if not matchesToken(TokenType.RIGHT_PAREN):
            raise ParseException("Expecting ')', found {0}".format(peekToken()[1]), peekToken())
        else:
            nextToken()
    elif matchesToken(TokenType.IDENTIFIER):
        result.type = ExprType.IDENTIFIER
        result.eval = evalVariableGet
        result.token = nextToken()
    else:
        result.type = ExprType.LITERAL
        result.eval = evalLiteral
        result.token = peekToken()
        if matchesToken(TokenType.FALSE):
            result.value = False
            result.dataType = DataType.BOOLEAN
        elif matchesToken(TokenType.TRUE):
            result.value = True
            result.dataType = DataType.BOOLEAN
        elif matchesToken(TokenType.NIL):
            result.value = None
            result.dataType = DataType.NIL
        elif matchesToken(TokenType.STRING):
            result.value = result.token[1]
            result.dataType = DataType.STRING
        elif matchesToken(TokenType.NUMBER):
            if result.token[1].find(".") > -1:
                result.value = float(result.token[1])
                result.dataType = DataType.DOUBLE
            else:
                result.value = int(result.token[1])
                result.dataType = DataType.INTEGER
        nextToken()

    return result


def peekToken(lookAhead=0):
    if isEndOfTokens():
        return None
    else:
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


def matchesToken(*tokenTypes):
    if tokenTypes[0] is TokenType:
        currToken = tokenTypes[0]
        del tokenTypes[0]
    else:
        currToken = peekToken()

    if currToken is not None:
        for tokenType in tokenTypes:
            if tokenType == currToken[0]:
                return True
    return False


def isEndOfTokens(offset=0):
    return currIdx + offset >= len(tokens)


def consume(tokenType):
    token = peekToken()
    if token is None:
        raise ParseException("Expected {0}, no more tokens found".format(tokenType), token)
    elif token[0] != tokenType:
        raise ParseException("Expected {0}, found {1}".format(tokenType, token[1]), token)
    else:
        nextToken()
