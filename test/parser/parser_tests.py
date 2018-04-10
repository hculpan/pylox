import unittest
import sys

from pylox.parser.parser import parse
from pylox.lexer.scanner import tokenize


class MyTest(unittest.TestCase):

    def test_primary_1(self):
        print("Running {0}".format(sys._getframe().f_code.co_name))
        tokens = tokenize("true", 0)
        ast = parse(tokens)
        while ast is not None:
            print(ast)
            ast = ast.right

    def test_primary_2(self):
        print("Running {0}".format(sys._getframe().f_code.co_name))
        tokens = tokenize('true false nil "A string" 12.09', 0)
        ast = parse(tokens)
        while ast is not None:
            print(ast)
            ast = ast.right

    def test_grouping1(self):
        print("Running {0}".format(sys._getframe().f_code.co_name))
        tokens = tokenize('12.09("a")', 0)
        ast = parse(tokens)
        while ast is not None:
            print(ast)
            ast = ast.right

    def test_grouping2(self):
        print("Running {0}".format(sys._getframe().f_code.co_name))
        tokens = tokenize('12.09("a")-3', 0)
        ast = parse(tokens)
        while ast is not None:
            print(ast)
            ast = ast.right

    def test_unary(self):
        print("Running {0}".format(sys._getframe().f_code.co_name))
        tokens = tokenize('-12.09', 0)
        ast = parse(tokens)
        while ast is not None:
            print(ast)
            ast = ast.right
