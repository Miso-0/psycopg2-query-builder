import psycopg2
from querybuilder.builder import QueryBuilder

database_connection = psycopg2.connect(
    database='todo_app',
    host='localhost',
    user='misomenze',
    password='local',
    port=5432,
)


def _cursor():
    db_curser = database_connection.cursor()
    return db_curser


query = QueryBuilder(_cursor())

res = (
    query.select("*")
    .table("users")
    .equal("id", "31cf8291-1901-494b-ba82-6f27a6744cb9")
    .equal("email", "test@gmail.com")
    .execute()
)

print(res)