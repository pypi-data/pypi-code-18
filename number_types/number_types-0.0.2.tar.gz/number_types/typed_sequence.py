# This should NOT be committed

# TODO

from typing import List, Any, GenericMeta, Union, Optional, Iterable
from abc import ABCMeta

def matches_type(type: Union[ABCMeta, type], object: Any) -> bool:
    if isinstance(type, GenericMeta):
        if hasattr(type, '__args__'):
            pass


class TypedList(list):
    def __init__(self, iterable: Optional[Iterable]=None, typing: GenericMeta=List[Any, ...]) -> None:
        if iterable is None:
            pass

# This should NOT be committed
