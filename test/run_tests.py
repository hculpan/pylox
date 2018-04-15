import unittest

from pylox.run import runLine
from pylox.interpreter.Data import DataType
from pylox.exceptions.RuntimeException import RuntimeException


class RunTests(unittest.TestCase):

    def test_run_1(self):
        result = runLine(0, "1;")
        assert result[0] == 1
        assert result[1] == DataType.INTEGER

    def test_run_2(self):
        result = runLine(0, "true;")
        assert result[0] == True
        assert result[1] == DataType.BOOLEAN

    def test_run_3(self):
        result = runLine(0, '"This is true";')
        assert result[0] == 'This is true'
        assert result[1] == DataType.STRING

    def test_run_4(self):
        result = runLine(0, "(4);")
        assert result[0] == 4
        assert result[1] == DataType.INTEGER

    def test_run_5(self):
        result = runLine(0, "-4.0;")
        assert result[0] == -4
        assert result[1] == DataType.DOUBLE

    def test_run_6(self):
        result = runLine(0, "1 * 2;")
        assert result[0] == 2
        assert result[1] == DataType.INTEGER

    def test_run_7(self):
        result = runLine(0, "3 * 2.0;")
        assert result[0] == 6
        assert result[1] == DataType.DOUBLE

    def test_run_8(self):
        result = runLine(0, "3 * 8 / 2;")
        assert result[0] == 12
        assert result[1] == DataType.DOUBLE

    def test_run_9(self):
        result = runLine(0, "3 + 8;")
        assert result[0] == 11
        assert result[1] == DataType.INTEGER

    def test_run_10(self):
        result = runLine(0, "3 + 8 * 2;")
        assert result[0] == 19
        assert result[1] == DataType.INTEGER

    def test_run_11(self):
        result = runLine(0, "(3 + 8) * 2;")
        assert result[0] == 22
        assert result[1] == DataType.INTEGER

    def test_run_12(self):
        result = runLine(0, "(3 + 8) / 2;")
        assert result[0] == 5.5
        assert result[1] == DataType.DOUBLE

    def test_run_13(self):
        result = runLine(0, "3 + 8 / 2;")
        assert result[0] == 7
        assert result[1] == DataType.DOUBLE

    def test_run_14(self):
        result = runLine(0, "(3 + 8) / -2;")
        assert result[0] == -5.5
        assert result[1] == DataType.DOUBLE

    def test_run_15(self):
        result = runLine(0, '"Hel" + "lo";')
        assert result[0] == "Hello"
        assert result[1] == DataType.STRING

    def test_run_16(self):
        result = runLine(0, "1 < 2;")
        assert result[0] is True
        assert result[1] == DataType.BOOLEAN

    def test_run_17(self):
        result = runLine(0, "10 * 2 < 6 * 5;")
        assert result[0] is True
        assert result[1] == DataType.BOOLEAN

    def test_run_18(self):
        result = runLine(0, "10 * 2 > 6 * 5;")
        assert result[0] is False
        assert result[1] == DataType.BOOLEAN

    def test_run_19(self):
        result = runLine(0, "false < true;")
        assert result[0] is True
        assert result[1] == DataType.BOOLEAN

    def test_run_20(self):
        result = runLine(0, "true < false;")
        assert result[0] is False
        assert result[1] == DataType.BOOLEAN

    def test_run_21(self):
        result = runLine(0, '"abc" < "bca";')
        assert result[0] is True
        assert result[1] == DataType.BOOLEAN

    def test_run_22(self):
        result = runLine(0, '"bca" < "abc";')
        assert result[0] is False
        assert result[1] == DataType.BOOLEAN

    def test_run_23(self):
        try:
            result = runLine(0, '"abc" < 1;')
        except RuntimeException as err:
            assert True
        else:
            assert False

    def test_run_24(self):
        result = runLine(0, '"bca" == "abc";')
        assert result[0] is False
        assert result[1] == DataType.BOOLEAN

    def test_run_25(self):
        result = runLine(0, '"bca" != "abc";')
        assert result[0] is True
        assert result[1] == DataType.BOOLEAN

    def test_run_26(self):
        result = runLine(0, '-(-2);')
        assert result[0] == 2
        assert result[1] == DataType.INTEGER

