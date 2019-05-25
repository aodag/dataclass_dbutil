import dataclasses
import pytest


@dataclasses.dataclass()
class Person:
    id: int = dataclasses.field()
    name: str = dataclasses.field()
    age: int = dataclasses.field()


CREATE_TABLE = """\
CREATE TABLE person
(
    id integer primary key,
    name varchar,
    age int
)
"""
DROP_TABLE = """\
DROP TABLE person
"""
INSERT_PERSON = """\
INSERT INTO person (name, age) VALUES (?, ?)
"""


@pytest.fixture
def dummy_db():
    import sqlite3

    db = sqlite3.connect(":memory:")
    cur = db.cursor()
    cur.execute(CREATE_TABLE)
    cur.execute(INSERT_PERSON, ("dummy", 17))
    cur.close()
    try:
        yield db
    finally:
        cur = db.cursor()
        cur.execute(DROP_TABLE)
        cur.close()
        db.close()


def test_it(dummy_db):
    from dataclass_dbutil.query import ResultMapper

    result = ResultMapper(dummy_db).query(Person, "SELECT id, name, age FROM person")
    assert result[0].name == "dummy"
