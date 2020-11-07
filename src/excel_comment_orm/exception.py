class ECOException(Exception):
    pass

class ECOWarning(Warning):
    pass

class TooManyBeginException(ECOException):
    pass


class TooManyEndException(ECOException):
    pass


class ExpectEndException(ECOException):
    pass


class BadTemplateException(ECOException):
    pass

class CommentWithNoECOBlockWarning(ECOWarning):
    pass
