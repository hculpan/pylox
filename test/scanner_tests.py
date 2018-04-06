import unittest

from pylox.scanner import tokenize


class MyTest(unittest.TestCase):

    def test_simple_1(self):
        s = "This is a test"
        l = tokenize(s)
        assert len(l) == 4

    def test_simple_2(self):
        s = "Thisisatest"
        l = tokenize(s)
        assert len(l) == 1

    def test_simple_3(self):
        s = "This is.a test"
        l = tokenize(s)
        assert len(l) == 5
        assert l[0] == "This"
        assert l[1] == "is"
        assert l[2] == "."
        assert l[3] == "a"
        assert l[4] == "test"

    def test_simple_3(self):
        s = 'This is "a" test!'
        l = tokenize(s)
        assert len(l) == 7
        assert l[0] == "This"
        assert l[1] == "is"
        assert l[2] == '"'
        assert l[3] == "a"
        assert l[4] == '"'
        assert l[5] == "test"
        assert l[6] == "!"


if __name__ == '__main__':
    unittest.main()