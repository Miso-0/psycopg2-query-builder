from typing import Union
from querybuilder.builder_errors import QueryErrors
from querybuilder import Table, Column, Function


class QueryBuilder:
    def __init__(self, cursor):
        """
        Initialize the QueryBuilder with a database cursor.

        Args:
            cursor: A database cursor to execute SQL queries.
        """
        self._query = ""
        self._table = ""
        self._schema = ""
        self._cursor = cursor
        self._specified_columns = []
        self._where_called = False
        self._table_called = False
        self._select_called = False
        self._join_called = False
        self._on_called = False
        self._function_called = False

    def __eq__(self, other):
        if isinstance(other, QueryBuilder):
            return self._query == other._query
        return False

    def __str__(self) -> str:
        return self._query

    def select(self, columns: Union[list[Column], str] = "*") -> "QueryBuilder":
        """
        Specifies the columns to select in the SQL query.

        Args:
            columns: A list of column names or a string '*' to select all columns.
                    =============================================================================================
                    NOTE: make sure that the columns list is ordered the same as expected columns to be returned
                          from the sql query otherwise the resulting keys and values will be mismatched
                    =============================================================================================

        Returns:
            QueryBuilder: The current instance to allow method chaining.
        """
        if self._select_called:
            raise QueryErrors("`select` has already been called.")
        self._select_called = True

        if columns == "*":
            self._query = "SELECT * FROM"  # Select all columns
        else:
            self._specified_columns = columns if isinstance(columns, list) else [columns]
            self._query = f"SELECT {', '.join(self._specified_columns.__str__())} FROM"  # Select specified columns
        return self

    def table(self, table: Table) -> "QueryBuilder":
        """
        Specifies the table to query.

        Args:
            table: The name of the table to query.

        Returns:
            QueryBuilder: The current instance to allow method chaining.
            :param table:
        """
        if not self._select_called:
            raise QueryErrors("`table` method must be called after `select`.")
        if self._table_called:
            raise QueryErrors("`table` has already been called.")

        self._table = table
        self._query += f" {table.__str__()}"
        self._table_called = True

        return self

    def function(self, function: Function) -> "QueryBuilder":
        if len(self._specified_columns) == 0:
            raise QueryErrors("Specify the expected return columns on 'select' when using 'function'")

        self._query += f" {function.__str__()}"
        self._table_called = True
        self._function_called = True
        return self

    def equal(self, column: str, value) -> "QueryBuilder":
        """
        Adds a WHERE clause to the query for equality comparison.

        Args:
            column: The column name to compare.
            value: The value to compare the column against.

        Returns:
            QueryBuilder: The current instance to allow method chaining.
        """
        if not self._table_called:
            raise QueryErrors("`equal` method must be called after `table`.")
        clause = f"{column.__str__()}='{value}'"
        self._query += f" {'AND' if self._where_called else 'WHERE'} {clause}"
        self._where_called = True
        return self

    def join_on(self, table: str, column1: str, column2: str) -> "QueryBuilder":
        if not self._table_called:
            raise QueryErrors("`equal` method must be called after `table`.")

        if self._where_called:
            raise QueryErrors("`where` should be called after all the `join` and `on` methods are called")

        self._on_called = True

        self._query += f" JOIN {table} {'AND' if self._on_called else 'ON'} {self._table}.{column1} = {table}.{column2}"
        return self

    def execute(self) -> list[dict]:
        """
        Executes the constructed SQL query and returns the results.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents a row in the result set.

        Raises:
            QueryErrors: If the query is incomplete (i.e., `select` and `table` have not been called).
        """
        if not (self._select_called and self._table_called):
            raise QueryErrors("Incomplete query. Make sure `select` and `table` have been called.")

        try:
            self._cursor.execute(self._query)
            data = self._cursor.fetchall()
            if not data:
                return []

            data_columns = self._specified_columns or self._get_table_columns()
            return self._map_columns_to_values(data_columns, data)
        except Exception as e:
            raise QueryErrors(e.__str__())

    def _get_table_columns(self) -> list[str]:
        """
        Retrieves the column names for the current table from the database.

        Returns:
            list[str]: A list of column names for the table.
        """
        self._cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s;",
                             (self._table,))
        return [column[0] for column in self._cursor.fetchall()]

    @staticmethod
    def _map_columns_to_values(columns: list[str], values: list[tuple]) -> list[dict]:
        """
        Maps column names to their corresponding values for each row.

        Args:
            columns: A list of column names.
            values: A list of tuples, where each tuple represents a row of values.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary maps column names to row values.
        """
        return [{col: val for col, val in zip(columns, row)} for row in values]
