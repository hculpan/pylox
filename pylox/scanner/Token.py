class Token:
    def __init__(self, type, text, linePos, lineNo):
        self.type = type
        self.text = text
        self.linePos = linePos
        self.lineNo = lineNo
