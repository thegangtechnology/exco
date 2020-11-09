import abc


class SpecSource(abc.ABC):
    @abc.abstractmethod
    def describe(self) -> str:
        """

        Returns:
            str to print incase there is an error constructing extractor for tracing back
        """
        raise NotImplementedError()

class UnknownSource(SpecSource):

    def describe(self) -> str:
        return 'Unknown Source'

