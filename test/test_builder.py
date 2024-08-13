import pytest

from querybuilder.builder import QueryBuilder


def test_select():
    builder = QueryBuilder(None)
    query = builder.select("*").__str__()
    assert query == "SELECT * FROM"


def test_table():
    builder = QueryBuilder(None)
    query = builder.select("*").table("users").__str__()
    assert query == "SELECT * FROM users"


def test_equal_no_table_called():
    builder = QueryBuilder(None)
    with pytest.raises(ValueError) as e:
        query = builder.select("*").equal("id", 1).__str__()
        assert query == "SELECT * FROM users WHERE id='1'"
    assert str(e.value) == "`equal` method must be called after `table`."


def test_equal():
    builder = QueryBuilder(None)
    query = builder.select("*").table("users").equal("id", 1).__str__()
    assert query == "SELECT * FROM users WHERE id='1'"


def test_equal_x_2():
    builder = QueryBuilder(None)
    query = builder.select("*").table("users").equal("id", 1).equal("email", "test@gmail.com").__str__()
    assert query == "SELECT * FROM users WHERE id='1' AND email='test@gmail.com'"


def test_specified_columns():
    builder = QueryBuilder(None)
    query = builder.select("id,email").table("users").equal("id", 1).__str__()
    assert query == "SELECT id,email FROM users WHERE id='1'"
