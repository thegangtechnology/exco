from dataclasses import dataclass
from typing import Optional


@dataclass
class TableEndConditionResult:
    """
    Table End Conditon Result
    """
    should_terminate: bool
    is_inclusive: bool  # should the row that end condition evaluates to true be included in the results
    is_ok: bool
    msg: str = ''
    exception: Optional[Exception] = None

    @property
    def is_exclusive(self) -> bool:
        """

        Returns:
            bool. True if the row that the condition is evaluated to True should be excluded
            from the result.
        """
        return not self.is_inclusive

    @classmethod
    def good(cls, should_terminate: bool, is_inclusive: bool) -> 'TableEndConditionResult':
        """Good TableEndConditionResult

        Args:
            should_terminate (bool):
            is_inclusive (bool):

        Returns:
            TableEndConditionResult
        """
        return TableEndConditionResult(
            should_terminate=should_terminate,
            is_inclusive=is_inclusive,
            is_ok=True
        )

    @classmethod
    def bad(cls, msg: str = '', exception: Optional[Exception] = None) -> 'TableEndConditionResult':
        """Bad TableEndConditionResult

        Args:
            msg (str):
            exception ():

        Returns:
            TableEndConditionResult
        """
        return TableEndConditionResult(
            should_terminate=True,
            is_inclusive=False,
            is_ok=False,
            msg=msg,
            exception=exception
        )
