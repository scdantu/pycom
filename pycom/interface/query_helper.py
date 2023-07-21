import pandas as pd
import sqlite3


def query_database(query, db_path):
    conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
