class ExcoException(RuntimeError):
    def __init__(self, msg: str = ''):
        super().__init__(msg)
        self.msg = msg


class ExcoWarning(Warning):
    pass


class TooManyBeginException(ExcoException):
    pass


class TooManyEndException(ExcoException):
    pass


class ExpectEndException(ExcoException):
    pass


class BadTemplateException(ExcoException):
    pass


class CommentWithNoExcoBlockWarning(ExcoWarning):
    pass


class ExcoBlockContainsExtraKey(ExcoException):
    pass


class ActorCreationFailException(ExcoException):
    pass


class ParserCreationFailException(ExcoException):
    pass


class ParserSpecCreationException(ExcoException):
    pass


class ParsingFailException(ExcoException):
    pass


class ExtractionTaskCreationException(ExcoException):
    pass


class ExcelProcessorCreationException(ExcoException):
    pass


class TooManyRowRead(ExcoException):
    pass


class TableKeyNotFound(ExcoException):
    pass


class TableHasNoColumn(ExcoException):
    pass


class MissingTableBlock(ExcoException):
    pass


class TableExtractionTaskCreationException(ExcoException):
    pass


class NoEndConditonError(ExcoException):
    pass


class YamlParseError(ExcoException):
    pass
