# QueryBuilder for Psycopg2

QueryBuilder is a lightweight Python package designed to simplify building SQL queries when using the Psycopg2 library to interact with PostgreSQL databases. Inspired by the design and functionality of Supabase's client SDKs, QueryBuilder aims to provide an intuitive and fluid API for constructing and executing SQL queries.

## Features

- Chainable methods for building SQL queries in a readable and maintainable manner.
- Support for `SELECT` statements with conditional filters.
- Automatic mapping of query results to a list of dictionaries for easier data manipulation.
- Designed to prevent common SQL query construction errors.

## Installation

You can install QueryBuilder using pip:

```bash
pip install querybuilder
```

## Usage

Here's a quick example of how to use the QueryBuilder in your project:

```python
from internal.database.db import QueryBuilder
from dotenv import dotenv_values
import psycopg2

# Load environment variables
env_config = dotenv_values(".env")

# Establish a database connection
database_connection = psycopg2.connect(
    database=env_config.get("DB_NAME"),
    host=env_config.get("DB_HOST"),
    user=env_config.get("DB_USER"),
    password=env_config.get("DB_PASSWORD"),
    port=env_config.get("DB_PORT"),
)

# Function to get a database cursor
db_curser = database_connection.cursor()

# Create a QueryBuilder instance
query = QueryBuilder(db_curser)

# Build and execute a query
res = (
    query.select("*")
    .table("users")
    .equal("id", "uuid")
    .equal("email", "test@gmail.com")
    .execute()
)

# Print the result
print(res)

res = (
    query.select(["id","email","hashed_password"])
    .table("users")
    .equal("id", "uuid")
    .execute()
)

print(res)
```

### Explanation:

- **Environment Configuration:** The `dotenv_values` function is used to load environment variables from a `.env` file, which includes database connection details.
- **Database Connection:** A connection to the PostgreSQL database is established using Psycopg2.
- **Cursor Function:** The `_cursor()` function returns a new database cursor, which is passed to the `QueryBuilder`.
- **Query Construction:** The `select()` method specifies the columns to be retrieved (`*` means all columns), and the `table()` method specifies the table to query (`users`).
- **Query Execution:** The `execute()` method runs the query and returns the results as a list of dictionaries.

## License

This project is licensed under the MIT License.
