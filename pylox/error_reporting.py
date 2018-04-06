errorFound = False


def hasError():
    global errorFound
    return errorFound


def clearError():
    global errorFound
    errorFound = False


def error(message, lineNo = 0):
    report(lineNo, "", message)


def report(lineNo, where, message):
    global errorFound
    errorFound = True
    if lineNo == 0:
        print("Error {1}: {2}".format(lineNo, where, message))
    else:
        print("[Line {0}] Error {1}: {2}".format(lineNo, where, message))