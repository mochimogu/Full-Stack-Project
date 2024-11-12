import psycopg2
import os
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor
from contextlib import contextmanager
from flask import Flask, jsonify, json
from dotenv import load_dotenv

pool = None
load_dotenv()

def setup():
    global pool
    DATABASE_URL = os.getenv("FLASK_DATABASE")
    pool = ThreadedConnectionPool(1, 100, dsn=DATABASE_URL, sslmode='require')
    
setup()

@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)

@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()
          
def createTable():
    with get_db_cursor(True) as cur:
        query = """CREATE TABLE CRUD (
            CRUD_ID SERIAL PRIMARY KEY,
            CONTENT VARCHAR(256),
            LAST_EDIT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CREATED DATE DEFAULT CURRENT_DATE
        )"""
        
        cur.execute(query)
    
# createTable();








