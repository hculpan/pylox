import unittest

from pylox.lexer.scanner import tokenize, TokenType


class MyTest(unittest.TestCase):

    def test_simple_1(self):
        s = "This is a test"
        l = tokenize(s)
        assert len(l) == 5

    def test_simple_2(self):
        s = "Thisisatest"
        l = tokenize(s)
        assert len(l) == 2

    def test_simple_3(self):
        s = "This is.a test"
        l = tokenize(s)
        assert len(l) == 6
        assert l[0][1] == "This"
        assert l[1][1] == "is"
        assert l[2][1] == "."
        assert l[3][1] == "a"
        assert l[4][1] == "test"

    def test_simple_4(self):
        s = 'This is "a" test!'
        l = tokenize(s)
        assert len(l) == 6
        assert l[0][1] == "This"
        assert l[0][0] == TokenType.IDENTIFIER
        assert l[1][1] == "is"
        assert l[1][0] == TokenType.IDENTIFIER
        assert l[2][1] == "a"
        assert l[2][0] == TokenType.STRING
        assert l[3][1] == "test"
        assert l[3][0] == TokenType.IDENTIFIER
        assert l[4][1] == "!"
        assert l[4][0] == TokenType.BANG
        assert l[5][0] == TokenType.EOL


if __name__ == '__main__':
    unittest.main()