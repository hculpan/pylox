class ParseException(Exception):
    def __init__(self, message, token=None):
        self.message = message
        self.token = token