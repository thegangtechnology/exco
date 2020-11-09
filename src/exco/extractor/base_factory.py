import abc
from typing import TypeVar, Generic, Dict, Type, List

from exco import util
from exco.exception import ParserCreationFailException
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
        raise NotImplementedError()

    @classmethod
    def key_for_class(cls, clz: Type[ActorType]) -> str:
        return util.default_key(clz, suffix=cls.suffix())

    @classmethod
    def build_class_dict(cls, classes: List[ActorType]) -> Dict[str, Type[ActorType]]:
        return {cls.key_for_class(clz): clz for clz in classes}

    def register(self, clz: Type[ActorType]):
        key = self.key_for_class(clz)
        self.class_map[key] = clz

    def register_all(self, classes: List[Type[ActorType]]):
        for c in classes:
            self.register(c)

    def available_keys(self) -> List[str]:
        return list(self.class_map.keys())

    def create_from_spec(self, spec: SpecType) -> ActorType:
        suffix = self.suffix()
        if spec.name not in self.class_map:
            raise ParserCreationFailException(f'Cannot find {suffix} for name {spec.name}\n'
                                              f'available keys are {list(self.class_map.keys())}')
        clz = self.class_map[spec.name]
        try:
            return clz.create(params=spec.params)
        except Exception as e:
            raise ParserCreationFailException(
                f'Unable to construct {suffix} from spec {spec}') from e
