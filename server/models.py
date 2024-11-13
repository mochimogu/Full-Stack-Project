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

def getAll():
    with get_db_cursor(True) as cur:
        
        query = """SELECT * FROM CRUD"""
        
        cur.execute(query)
        
        results = cur.fetchall()
        
        return results
    
def getByID(id):
    with get_db_cursor(True) as cur:
        query = """SELECT CONTENT FROM CRUD WHERE CRUD_ID=%s;"""
        cur.execute(query, (id,))
        
        results = cur.fetchone()
        
        return results
        

def insert(data):
    with get_db_cursor(True) as cur:
        query = """INSERT INTO CRUD (CONTENT) VALUES (%s);"""
        cur.execute(query, (data,))
        

def update(id, content):
    with get_db_cursor(True) as cur:
        # print(id, content)
        query = """UPDATE CRUD SET CONTENT = %s, LAST_EDIT = CURRENT_TIMESTAMP WHERE CRUD_ID = %s;"""
        cur.execute(query, (content, id))
        if cur.rowcount > 0:
            return 0
        else:
            return -1
        
def delete(id):
    with get_db_cursor(True) as cur:
        query = """DELETE FROM CRUD WHERE CRUD_ID = %s;"""
        cur.execute(query, (id,))
        if cur.rowcount > 0:
            return 0
        else:
            return -1