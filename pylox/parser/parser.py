from pylox.ast.Expr import Expr
from pylox.interpreter.ExprEvals import *
from pylox.interpreter.Data import DataType
from pylox.scanner.scanner import TokenType
from pylox.exceptions.ParseException import ParseException

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
    elif matchesToken(TokenType.FUN):
        result = funDecl()
    else:
        result = statement()
    return result


def funDecl():
    expr = Expr(ExprType.FUNCTION, nextToken())
    if not matchesToken(TokenType.IDENTIFIER):
        raise ParseException("Expected fucntion identifier, found {0}".format(peekToken().text), peekToken())
    expr.value = consume(TokenType.IDENTIFIER).text
    expr.left = parameters()
    expr.right = block()
    expr.eval = evalFunc
    return expr


def parameters():
    params = list()

    consume(TokenType.LEFT_PAREN)
    if not matchesToken(TokenType.RIGHT_PAREN):
        params.append(consume(TokenType.IDENTIFIER))
        while matchesToken(TokenType.COMMA):
            consume(TokenType.COMMA)
            params.append(consume(TokenType.IDENTIFIER))

    consume(TokenType.RIGHT_PAREN)

    return params


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

    consume(TokenType.SEMICOLON)
    return expr


def statement():
    if matchesToken(TokenType.PRINT):
        return printStmt()
    elif matchesToken(TokenType.LEFT_BRACE):
        return block()
    elif matchesToken(TokenType.IF):
        return ifStmt()
    elif matchesToken(TokenType.WHILE):
        return whileStmt()
    elif matchesToken(TokenType.RETURN):
        return returnStmt()
    elif matchesToken(TokenType.FOR):
        return forStmt()
    else:
        return exprStmt()


def returnStmt():
    expr = Expr(ExprType.RETURN, nextToken())
    expr.eval = evalReturn
    if not matchesToken(TokenType.SEMICOLON):
        expr.right = expr.right = expression()
    consume(TokenType.SEMICOLON)
    return expr


def forStmt():
    expr = Expr(ExprType.FOR, nextToken())
    consume(TokenType.LEFT_PAREN)

    if matchesToken(TokenType.VAR):
        expr.left = varDecl()
    elif not matchesToken(TokenType.SEMICOLON):
        expr.left = exprStmt()
    else:
        consume(TokenType.SEMICOLON)

    if not matchesToken(TokenType.SEMICOLON):
        expr.condition = expression()
    consume(TokenType.SEMICOLON)

    if not matchesToken(TokenType.RIGHT_PAREN):
        expr.increment = expression()
    consume(TokenType.RIGHT_PAREN)

    expr.right = statement()
    expr.eval = evalFor
    return expr


def whileStmt():
    token = nextToken()
    consume(TokenType.LEFT_PAREN)
    conditional = expression()
    consume(TokenType.RIGHT_PAREN)
    body = statement()

    expr = Expr(ExprType.WHILE, token)
    expr.condition = conditional
    expr.right = body
    expr.eval = evalWhile
    return expr


def ifStmt():
    expr = Expr(ExprType.IF, nextToken())
    expr.eval = evalIf
    consume(TokenType.LEFT_PAREN)
    expr.condition = expression()
    consume(TokenType.RIGHT_PAREN)
    expr.left = statement()
    if matchesToken(TokenType.ELSE):
        consume(TokenType.ELSE)
        expr.right = statement()
    return expr


def block():
    expr = Expr(ExprType.BLOCK, nextToken())
    expr.eval = evalBlock

    statements = list()
    while not matchesToken(TokenType.RIGHT_BRACE) and not isEndOfTokens():
        statements.append(declaration())

    consume(TokenType.RIGHT_BRACE)
    expr.right = statements
    return expr


def printStmt():
    expr = Expr(ExprType.PRINT)
    expr.token = nextToken()
    expr.eval = evalPrint
    expr.right = expression()
    consume(TokenType.SEMICOLON)
    return expr


def expression():
    expr = Expr()
    expr.eval = evalExpr
    return assignment()


def exprStmt():
    expr = expression()
    consume(TokenType.SEMICOLON)
    return expr


def assignment():
    expr = logicOr()

    if matchesToken(TokenType.EQUAL):
        assExpr = Expr(ExprType.ASSIGNMENT, nextToken())
        assExpr.eval = evalAssignment
        assExpr.left = expr
        assExpr.right = assignment()
        expr = assExpr

    return expr


def logicOr():
    expr = logicAnd()

    while matchesToken(TokenType.OR):
        token = nextToken()
        right = logicAnd()
        left = expr
        expr = Expr(ExprType.OR, token)
        expr.left = left
        expr.right = right
        expr.eval = evalLogical

    return expr


def logicAnd():
    expr = equality()
    while matchesToken(TokenType.AND):
        token = nextToken()
        right = equality()
        left = expr
        expr = Expr(ExprType.AND, token)
        expr.left = left
        expr.right = right
        expr.eval = evalLogical

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
        return call()


def call():
    expr = primary()
    if matchesToken(TokenType.LEFT_PAREN):
        callExpr = Expr(ExprType.CALL, nextToken())
        callExpr.left = expr
        callExpr.right = arguments()
        callExpr.eval = evalCall
        consume(TokenType.RIGHT_PAREN)
        expr = callExpr

    return expr


def arguments():
    args = list()

    if not matchesToken(TokenType.RIGHT_PAREN):
        arg = expression()
        if arg is not None:
            args.append(arg)
        while matchesToken(TokenType.COMMA):
            consume(TokenType.COMMA)
            arg = expression()
            if arg is not None:
                args.append(arg)
        return args
    else:
        return None


def primary():
    result = Expr()
    if matchesToken(TokenType.LEFT_PAREN):
        result.type = ExprType.GROUPING
        result.token = nextToken()
        result.right = addition()
        result.eval = evalGrouping
        if not matchesToken(TokenType.RIGHT_PAREN):
            raise ParseException("Expecting ')', found {0}".format(peekToken().text), peekToken())
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
            result.value = result.token.text
            result.dataType = DataType.STRING
        elif matchesToken(TokenType.NUMBER):
            if result.token.text.find(".") > -1:
                result.value = float(result.token.text)
                result.dataType = DataType.DOUBLE
            else:
                result.value = int(result.token.text)
                result.dataType = DataType.INTEGER
        nextToken()

    return result


def peekToken():
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
            if tokenType == currToken.type:
                return True
    return False


def isEndOfTokens(offset=0):
    return currIdx + offset >= len(tokens) or tokens[currIdx] == TokenType.EOF


def consume(tokenType):
    token = peekToken()
    if token is None:
        raise ParseException("Expected {0}, no more tokens found".format(tokenType), token)
    elif token.type != tokenType:
        raise ParseException("Expected {0}, found {1}".format(tokenType, token.text), token)
    else:
        return nextToken()
