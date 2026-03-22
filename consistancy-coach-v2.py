import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage

load_dotenv(override=True)

#Load goals
with open("goals.json", "r") as f:
    goals = json.load(f)

try:
    with open("progress.json", "r") as f:
        progress = json.load(f)
except:
    progress = {}

today = datetime.now().strftime("%Y-%m-%d")
days_until_exam = (datetime.strptime(goals["exam_date"], "%Y-%m-%d") - datetime.now()).days

print(f"Days until exam: {days_until_exam}")
print(f"Goals loaded: {goals['goals']}")

llm = ChatGroq(model="llama-3.3-70b-versatile")
search = TavilySearch(max_results=2)
tools = [search]
memory = MemorySaver()

system_prompt = f"""
You are Amar's personal consistency coach. Keep him accountable and motivated.

What you know about Amar:
- Goals: {goals['goals']}
- Exam subjects: {goals['subjects']}
- Exam date: {goals['exam_date']}
- Days until exam: {days_until_exam}
- Past progress: {progress}
- Today: {today}

Your behavior:
- Check in on yesterday's tasks
- Track what Amar completes each day
- Warn him when exams are getting close
- Be encouraging but honest
- Search for resources when he's stuck
- Keep responses concise and motivating
"""

agent = create_agent(
    llm, tools, checkpointer=memory, system_prompt=system_prompt
)

config = {"configurable": {"thread_id": "amar_coach"}}

print("\nConsistency Coach ready. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        progress[today] = {"session": "completed"}
        with open("progress.json", "w") as f:
            json.dump(progress, f)
        print("Progress saved. See you tomorrow!")
        break

    result = agent.invoke({
        "messages":[
            {"role": "user", 
             "content": user_input}
        ]
    },
    config=config)

    print(f"\nCoach: {result['messages'][-1].content}\n")

