from dotenv import load_dotenv
from llm import init_llm

load_dotenv()

llm = init_llm()
response = llm.invoke("What is today date and day?")
print(response.content)