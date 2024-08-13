import psycopg2
from querybuilder import QueryBuilder

database_connection = psycopg2.connect(
    database='faaster_demo',
    host='localhost',
    user='miso',
    password='local',
    port=5432,
)

db_curser = database_connection.cursor()

query = QueryBuilder(db_curser)

res = (
    query.select(['title']).rpc(schema="internal", params=[1], function='get_settings').execute()
)

print(res)
