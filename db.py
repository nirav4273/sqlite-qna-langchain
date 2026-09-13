import sqlite3

from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase


conn = sqlite3.connect("todo.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date DATE,
        status TEXT NOT NULL DEFAULT 'pending'
    )
""")
conn.commit()
conn.close()

DB_INSTANCE = SQLDatabase.from_uri("sqlite:///todo.db")
