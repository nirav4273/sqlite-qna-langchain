
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

st.subheader("QnA Todo list")
st.caption("Langchain todo with SQLite")

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
