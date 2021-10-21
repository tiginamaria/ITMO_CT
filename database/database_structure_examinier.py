# This file helps to retrieve SQL command for table creation

import sqlite3


def sqlite_table_schema(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.execute("SELECT sql FROM sqlite_master WHERE name=?;", [table_name])
    sql = cursor.fetchone()[0]
    conn.close()
    return sql


# print('Input database name:')
database = input('Input database name:')
table = input('Input table name:')
print(sqlite_table_schema(database, table))
