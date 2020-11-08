class ECOException(RuntimeError):
    def __init__(self, msg: str = ''):
        super().__init__(msg)
        self.msg = msg


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


class ECOBlockContainsExtraKey(ECOException):
    pass


class ParserCreationFailException(ECOException):
    pass


class ParsingFailException(ECOException):
    pass


class ExtractionTaskCreationException(ECOException):
    pass


class ExcelProcessorCreationException(ECOException):
    pass
