class QueryBuilder:
    _query: str
    _specified_columns: list[str]
    _select_called: bool
    _table_called: bool
    _where_called: bool
    _cursor: any

    def __init__(self, cursor):
        self._select_called = False
        self._table_called = False
        self._where_called = False
        self._specified_columns = []
        self._cursor = cursor

    def select(self, columns: list[str] | str | None) -> "QueryBuilder":
        if self._select_called:
            raise ValueError("`select` has already been called.")
        self._select_called = True

        if columns == "*":
            self._query = "select * from"
        else:
            self._specified_columns = columns
            self._query = "select " + ", ".join(columns) + " from"
        return self

    def table(self, table: str) -> "QueryBuilder":
        if not self._select_called:
            raise ValueError("`table` method must be called after `select`.")
        if self._table_called:
            raise ValueError("`table` has already been called.")
        self._table_called = True

        self._query = f"{self._query} {table}"
        return self

    def equal(self, column: str, value) -> "QueryBuilder":
        if not self._table_called:
            raise ValueError("`equal` method must be called after `table`.")

        if self._where_called:
            self._query = f"{self._query} and {column}='{value}'"
        else:
            self._query = f"{self._query} where {column}='{value}'"
            self._where_called = True
        return self

    def rpc(self, name: str) -> dict:
        return {}

    def _tb_columns(self) -> list:
        c = self._cursor
        c.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'users'"
        )
        res = c.fetchall()
        extracted_values = [c[0] for c in res]
        return extracted_values

    @staticmethod
    def _map_undefined_columns(columns: list, values: list[tuple]) -> list[dict]:
        result = []
        for r in values:
            d = {}
            for i in range(len(columns)):
                d[columns[i]] = r[i] if i < len(r) else ""
            result.append(d)
        return result

    def execute(self) -> list[dict]:
        if not (self._select_called and self._table_called):
            raise ValueError(
                "Incomplete query. Make sure `select` and `table` have been called."
            )
        self._cursor.execute(self._query)
        data = self._cursor.fetchall()
        if len(data) == 0:
            return []

        if len(self._specified_columns) > 0:
            data_columns = self._specified_columns
        else:
            data_columns = self._tb_columns()

        mapped = QueryBuilder._map_undefined_columns(data_columns, data)
        return mapped
