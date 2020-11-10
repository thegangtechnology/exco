import abc
from typing import TypeVar, Generic, Dict, Type, List

from exco import util
from exco.exception import ActorCreationFailException
from exco.extractor.actor import Actor

ActorType = TypeVar('ActorType', bound=Actor)
SpecType = TypeVar('SpecType')
T = TypeVar('T')


class BaseFactory(abc.ABC, Generic[ActorType, SpecType]):
    def __init__(self, class_map: Dict[str, Type[ActorType]]):
        self.class_map = class_map

    @classmethod
    @abc.abstractmethod
    def suffix(cls):
        """class suffix for this factory

        Returns:

        """
        raise NotImplementedError()

    @classmethod
    def key_for_class(cls, clz: Type[ActorType]) -> str:
        """Compute Key for class. By default it's suffix removed snake-cased of the class name
        Ex: AllBlankTableEndCondition -> all_blank (suffix is specified in suffix())
        Args:
            clz (Type[ActorType]):

        Returns:
            str
        """
        return util.default_key(clz, suffix=cls.suffix())

    @classmethod
    def build_class_dict(cls, classes: List[ActorType]) -> Dict[str, Type[ActorType]]:
        """Build class dictionary.
        The key is by default the class name with the suffix removed and then snake case.
        Ex: AllBlankTableEndCondition -> all_blank (suffix is specified in suffix())

        Args:
            classes (List[ActorType]):

        Returns:
            Dict[str, Type[ActorType]]
        """
        return {cls.key_for_class(clz): clz for clz in classes}

    def register(self, clz: Type[ActorType]):
        """Register a single class
        Args:
            clz ():

        Returns:
            None
        """
        key = self.key_for_class(clz)
        self.class_map[key] = clz

    def register_all(self, classes: List[Type[ActorType]]):
        """Register All actor classes
        Args:
            classes(List[Type[ActorType]]) :
        Returns:
            None
        """
        for c in classes:
            self.register(c)

    def available_keys(self) -> List[str]:
        """

        Returns:
            List of all available keys.
        """
        return list(self.class_map.keys())

    def create_from_spec(self, spec: SpecType) -> ActorType:
        """Create Actor from the given spec

        Args:
            spec (SpecType):

        Returns:
            ActorType
        """
        suffix = self.suffix()
        if spec.name not in self.class_map:
            raise ActorCreationFailException(f'Cannot find {suffix} for name {spec.name}\n'
                                             f'available keys are {list(self.class_map.keys())}')
        clz = self.class_map[spec.name]
        try:
            return clz.create(params=spec.params)
        except Exception as e:
            raise ActorCreationFailException(
                f'Unable to construct {suffix} from spec {spec}') from e
