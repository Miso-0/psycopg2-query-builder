class QueryBuilder:
    def __init__(self, cursor):
        """
        Initialize the QueryBuilder with a database cursor.

        Args:
            cursor: A database cursor to execute SQL queries.
        """
        self._query = ""  # Stores the SQL query being constructed
        self._specified_columns = []  # List of specified columns for SELECT statement
        self._select_called = False  # Tracks if the `select` method has been called
        self._table_called = False  # Tracks if the `table` method has been called
        self._where_called = False  # Tracks if the `equal` method (WHERE clause) has been called
        self._cursor = cursor  # Database cursor for executing the query

    def select(self, columns: list[str] | str = "*") -> "QueryBuilder":
        """
        Specifies the columns to select in the SQL query.

        Args:
            columns: A list of column names or a string '*' to select all columns.

        Returns:
            QueryBuilder: The current instance to allow method chaining.
        """
        if self._select_called:
            raise ValueError("`select` has already been called.")
        self._select_called = True

        if columns == "*":
            self._query = "SELECT * FROM"  # Select all columns
        else:
            self._specified_columns = columns if isinstance(columns, list) else [columns]
            self._query = f"SELECT {', '.join(self._specified_columns)} FROM"  # Select specified columns
        return self

    def table(self, table: str) -> "QueryBuilder":
        """
        Specifies the table to query.

        Args:
            table: The name of the table to query.

        Returns:
            QueryBuilder: The current instance to allow method chaining.
        """
        if not self._select_called:
            raise ValueError("`table` method must be called after `select`.")
        if self._table_called:
            raise ValueError("`table` has already been called.")
        self._table_called = True
        self._query += f" {table}"  # Append table name to the query
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
            raise ValueError("`equal` method must be called after `table`.")
        clause = f"{column}='{value}'"
        self._query += f" {'AND' if self._where_called else 'WHERE'} {clause}"  # Add WHERE or AND clause
        self._where_called = True
        return self

    def execute(self) -> list[dict]:
        """
        Executes the constructed SQL query and returns the results.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents a row in the result set.

        Raises:
            ValueError: If the query is incomplete (i.e., `select` and `table` have not been called).
        """
        if not (self._select_called and self._table_called):
            raise ValueError("Incomplete query. Make sure `select` and `table` have been called.")

        self._cursor.execute(self._query)  # Execute the query
        data = self._cursor.fetchall()  # Fetch all rows from the query result
        if not data:
            return []

        data_columns = self._specified_columns or self._get_table_columns()  # Determine columns to map
        return self._map_columns_to_values(data_columns, data)  # Map columns to values and return result

    def _get_table_columns(self) -> list[str]:
        """
        Retrieves the column names for the current table from the database.

        Returns:
            list[str]: A list of column names for the table.
        """
        self._cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'users'")
        return [column[0] for column in self._cursor.fetchall()]  # Extract column names from the result set

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
        return [{col: val for col, val in zip(columns, row)} for row in values]  # Map columns to values in each row