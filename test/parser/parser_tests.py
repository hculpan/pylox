import unittest
import sys

from pylox.parser.parser import parse
from pylox.scanner.scanner import tokenize
from pylox.ast.Expr import ExprType


class MyTest(unittest.TestCase):

    def test_primary_1(self):
        print("Running {0}".format(sys._getframe().f_code.co_name))
        tokens = tokenize("true;", 0)
        ast = parse(tokens)
        assert ast.type == ExprType.EXPRESSION
        assert ast.left is None
        assert ast.right.type == ExprType.LITERAL
        print(ast)

    def test_primary_2(self):
        print("Running {0}".format(sys._getframe().f_code.co_name))
        tokens = tokenize('nil;', 0)
        ast = parse(tokens)
        assert ast.type == ExprType.EXPRESSION
        assert ast.left is None
        assert ast.right.type == ExprType.LITERAL
        print(ast)

    def test_unary(self):
        print("Running {0}".format(sys._getframe().f_code.co_name))
        tokens = tokenize('-12.09;', 0)
        ast = parse(tokens)
        print(ast)

    def test_grouping(self):
        print("Running {0}".format(sys._getframe().f_code.co_name))
        tokens = tokenize('(-12.09);', 0)
        ast = parse(tokens)
        print(ast)

    def test_multiplication1(self):
        print("Running {0}".format(sys._getframe().f_code.co_name))
        tokens = tokenize('2* 3;', 0)
        ast = parse(tokens)
        print(ast)

    def test_multiplication2(self):
        print("Running {0}".format(sys._getframe().f_code.co_name))
        tokens = tokenize('2* 3 * 4;', 0)
        ast = parse(tokens)
        print(ast)

    def test_addition1(self):
        print("Running {0}".format(sys._getframe().f_code.co_name))
        tokens = tokenize('1- 3 +4 ;', 0)
        ast = parse(tokens)
        print(ast)

    def test_addition2(self):
        print("Running {0}".format(sys._getframe().f_code.co_name))
        tokens = tokenize('1- (3 +4) ;', 0)
        ast = parse(tokens)
        print(ast)

    def test_addition3(self):
        print("Running {0}".format(sys._getframe().f_code.co_name))
        tokens = tokenize('20- 3 *4 ;', 0)
        ast = parse(tokens)
        print(ast)

    def test_comparison(self):
        print("Running {0}".format(sys._getframe().f_code.co_name))
        tokens = tokenize('20- 3 *4 > 15 + 2 ;', 0)
        ast = parse(tokens)
        print(ast)

    def test_equality(self):
        print("Running {0}".format(sys._getframe().f_code.co_name))
        tokens = tokenize('20- 3 *4 > 15 + 2 == 14 / 3;', 0)
        ast = parse(tokens)
        print(ast)