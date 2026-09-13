
from dotenv import load_dotenv
from constant import SYSTEM_PROMPT
from db import DB_INSTANCE
from llm import init_llm
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st

load_dotenv()


model = init_llm()
sqlToolKit = SQLDatabaseToolkit(llm=model, db=DB_INSTANCE)
memory = InMemorySaver()

agent = create_agent(
  model=model,
  tools=sqlToolKit.get_tools(),
  system_prompt=SYSTEM_PROMPT,
  checkpointer=memory
)
if 'messages' not in st.session_state:
    st.session_state.messages = []

st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.subheader("QnA Todo list")
st.caption("Langchain todo with SQLite")

with st.expander("What can I ask?"):
    st.markdown("""
The `todos` table has these columns:

| Column | Type | Notes |
|---|---|---|
| id | INTEGER | auto-incrementing primary key |
| title | TEXT | task description |
| date | DATE | due/associated date |
| status | TEXT | e.g. pending, done |

Example questions:
- What todos are pending?
- Show me all todos due this week.
- How many tasks are marked as done?
- Add a todo "Buy groceries" for tomorrow.
- Mark todo 3 as done.
- List all todos sorted by date.
""")

for messages in st.session_state.messages:
    st.chat_message(messages['role']).markdown(messages['content'])

input = st.chat_input("Ask Question")

if input:
    st.session_state.messages.append({
        'role': 'user',
        'content': input
    })
    st.chat_message('user').markdown(input)
    with st.chat_message('ai'):
        with st.spinner():
          
          response = agent.invoke(
            {"messages": [{"role": "user", "content": input}]},
            {
              'configurable': {
                'thread_id': '124'
              }
            }
          )
          st.markdown(response["messages"][-1].content)
          st.session_state.messages.append({
              'role': 'ai',
              'content': response["messages"][-1].content
          })
