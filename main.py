from querybuilder import QueryBuilder
from querybuilder.types import Column, Table
import psycopg2

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
    query.select(columns=[Column(name="title", alies="Name", table="settings")]).table(
        table=Table(name="settings", schema="internal")).equal("id", 1).execute()
)

print(res)
