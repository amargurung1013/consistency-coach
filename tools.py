from langchain_groq import ChatGroq
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
import os

load_dotenv(override=True)
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

llm = ChatGroq(model="llama-3.3-70b-versatile")

search = TavilySearch(max_results=2)

@tool
def calculator(expression: str) -> str:
    """Calculate a math expression. Input should be a valid math expression like '2 + 2' or '1234 * 5678'."""
    return str(eval(expression))

tools = [calculator, search]

agent = create_react_agent(llm, tools)

result = agent.invoke({"messages": [{"role": "user", "content": "What is the weather in Kathmandu?"}]})
print(result['messages'][-1].content)