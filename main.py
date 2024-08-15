import psycopg2
from querybuilder import QueryBuilder

database_connection = psycopg2.connect(
    database='todo_app',
    host='localhost',
    user='misomenze',
    password='local',
    port=5432,
)

db_curser = database_connection.cursor()

query = QueryBuilder(db_curser)

res = (
    query.select(["email"]).table(table="users").join("todos").on("user_id")
)

print(res)
