from typing import (
    Any,
    Dict,
    Sequence,
    Type,
    TypeVar,
    Iterable,
    Tuple,
    Callable,
    Generator,
    List,
)
from .protocols import IConnection, ICursor, Description

T = TypeVar("T")


class ResultMapper:
    def __init__(self, conn: IConnection) -> None:
        self.conn = conn

    def _row_map(
        self, row: Sequence[Any], desc: Description
    ) -> Iterable[Tuple[str, Any]]:
        for i, d in enumerate(desc):
            yield d[0], row[i]

    def _iter_result_dict(self, cur: ICursor) -> Iterable[Dict[str, Any]]:
        desc = cur.description
        for row in cur.fetchall():
            yield dict(self._row_map(row, desc))

    def iter_query(self, cls: Type[T], sql: str) -> Generator[T, T, None]:
        cur = self.conn.cursor()
        try:
            cur.execute(sql, {})
            for d in self._iter_result_dict(cur):
                c: Callable = cls
                yield c(**d)
        finally:
            cur.close()

    def query(self, cls: Type[T], sql: str) -> List[T]:
        return list(self.iter_query(cls, sql))
