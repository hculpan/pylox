from enum import Enum

class TokenType(Enum):
    LEFT_PAREN = 1
    RIGHT_PAREN = 2
    LEFT_BRACE = 3
    RIGHT_BRACE = 4
    COMMA = 5
    DOT = 6
    MINUS = 7
    PLUS = 8
    SEMICOLON = 9
    SLASH = 10
    STAR = 11
    BANG = 12
    BANG_EQUAL = 13
    EQUAL = 14
    EQUAL_EQUAL = 15
    GREATER = 16
    GREATER_EQUAL = 17
    LESS = 18
    LESS_EQUAL = 19
    IDENTIFIER = 20
    STRING = 21
    NUMBER = 22
    COMMENT = 23
    AND = 24
    CLASS = 25
    ELSE = 26
    FALSE = 27
    FUN = 28
    FOR = 29
    IF = 30
    NIL = 31
    OR = 32
    PRINT = 33
    RETURN = 34
    SUPER = 35
    THIS = 36
    TRUE = 37
    VAR = 38
    WHILE = 39
    EOF = 40
    WHITESPACE = 41

