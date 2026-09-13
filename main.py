import sqlite3

from dotenv import load_dotenv
from llm import init_llm
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

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

db = SQLDatabase.from_uri("sqlite:///todo.db")
model = init_llm()

toolKit = SQLDatabaseToolkit(llm=model, db=db)

SYSTEM_PROMPT = f"""You are a helpful assistant that answers questions about the user's
todo list by querying a SQLite database.

You have access to tools for inspecting the database schema and running read-only SQL
queries. The database dialect is {db.dialect}.

Rules:
- Always look at the available tables and their schema before writing a query if you
  are not already certain of the columns.
- Only write SELECT, INSERT, UPDATE, DLEETE queries. Never DROP or otherwise modify
  the database.
- Write syntactically correct {db.dialect} queries. Limit results to a reasonable
  number of rows (e.g. 20) unless the user asks for more.
- Double-check your query before executing it. If a query fails, read the error,
  fix the query, and try again rather than giving up.
- After getting the query results, answer the user's question in clear, plain
  language based on the actual data returned. Do not fabricate data that wasn't
  returned by a query.
- If the question cannot be answered using the todos table, say so instead of
  guessing.
"""

memory = InMemorySaver()
agent = create_agent(
  model=model,
  tools=toolKit.get_tools(),
  system_prompt=SYSTEM_PROMPT,
  checkpointer=memory
)

while True:
  query = input("Ask question: ")
  if query.lower() == 'break':
    break

  response = agent.invoke(
    {"messages": [{"role": "user", "content": query}]},
    {
      'configurable': {
        'thread_id': '124'
      }
    }
  )

  print(response["messages"][-1].content)