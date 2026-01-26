from typing import Any, Self


class ContextScope(dict):
    __slots__ = ('parent',)

    def __init__(self, parent: dict, **kwargs: dict) -> None:
        dict.__init__(self, **kwargs)
        self.parent = parent

    def __missing__(self, key: str) -> Any:  # noqa: ANN401
        return self.parent[key]

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: ANN001
        pass
