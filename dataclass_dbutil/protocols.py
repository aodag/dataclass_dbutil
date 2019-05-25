from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
from typing_extensions import Protocol

"""
name
type_code
display_size
internal_size
precision
scale
null_ok
"""

Description = List[
    Tuple[
        str,  # name
        str,  # type_code
        Optional[int],  # display_size
        Optional[int],  # internal_size
        Optional[int],  # precision
        Optional[int],  # scale
        Optional[bool],  # null_ok
    ]
]

Parameters = Union[List[Any], Dict[Any, Any]]


class ICursor(Protocol):
    description: Description
    rowcount: int

    def callproc(self, procname: str, parameters: Parameters) -> None:
        ...

    def close(self) -> None:
        ...

    def execute(self, operation: str, parameters: Parameters) -> None:
        ...

    def executemany(self, operation: str, parameters: Sequence[Parameters]) -> None:
        ...

    def fetchone(self) -> Sequence[Any]:
        ...

    def fetchmany(self) -> Sequence[Sequence[Any]]:
        ...

    def fetchall(self) -> Sequence[Sequence[Any]]:
        ...


class IConnection(Protocol):
    def close(self) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...

    def cursor(self) -> ICursor:
        ...
