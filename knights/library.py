from collections.abc import Callable
from functools import partial
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .lexer import Token
    from .parser import Parser

type TagType = Callable[[Parser, Token], Any]


class Library:
    """
    Container for registering tags and helpers
    """

    def __init__(self) -> None:
        self.tags = {}
        self.helpers = {}

    def tag(self, func: TagType | None = None, name: str | None = None) -> Callable:
        if func is None:
            return partial(self.tag, name=name)

        if name is None:
            name = func.__name__

        self.tags[name] = func
        return func

    def helper(self, func: Callable | None = None, name: str | None = None) -> Callable:
        if func is None:
            return partial(self.helper, name=name)

        if name is None:
            name = func.__name__

        self.helpers[name] = func
        return func
