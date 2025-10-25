# db.py
import mysql.connector
from mysql.connector import errorcode
from contextlib import contextmanager
import pandas as pd

config = {
    'host': 'localhost',       
    'port': 3306,
    'user': 'root',
    'password': 'lenovo@1975$',
    #'host': 'localhost:3306',
    'database': 'srms',
    'raise_on_warnings': True
}

'''
@contextmanager
def get_cursor(commit=False):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
'''
        
def get_connection():
    return mysql.connector.connect(**config)

def run_query(query, params=None, fetch=False):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchall() if fetch else None
    conn.commit()
    cursor.close()
    conn.close()
    return pd.DataFrame(result) if fetch else None
