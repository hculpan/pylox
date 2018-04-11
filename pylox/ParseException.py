class ParseException(Exception):
    def __init__(self, message, lineNo):
        self.message = message
        self.lineNo = lineNo