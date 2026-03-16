import os
import json
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

load_dotenv(override=True)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

#load goals
with open("goals.json", "r") as f:
    goals = json.load(f)

#load progess
try:
    with open("progress.json", "r") as f:
        progress = json.load(f)
except:
    progress = {}

#get today's date
today = datetime.now().strftime("%Y-%m-%d")
days_until_exam = (datetime.strptime(goals["exam_date"], "%Y-%m-%d") - datetime.now()).days

print(f"Today: {today}")
print(f"Days until exam: {days_until_exam}")
print(f"Goals: {goals['goals']}")

system_prompt = f"""You are Amar's personal consistency coach. Your job is to keep him accountable and motivated.

Here is what you know about Amar:
- Goals: {goals['goals']},
- Exam subjects: {goals['subjects']},
- Exam date: {goals['exam_date']},
- Days until exam: {days_until_exam},
- Past progress: {progress}
- Today's date: {today}

Your behavior: 
- Check in on yersterday's task if it's a new day
- Track what Amar completes each day
- Warn him when exams are getting close
- Be encouraging but honest - call him out if he's slipping
- If he's stuck on something, offer to search for resources
- Keep responses concise and motivating

If you need to search the web, say exactly: 
SEARCH: <query>

Otherwise just respond normally."""

conversation_history = [{"role": "system", "content": system_prompt}]
print("\nConsistency coach ready. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        progress[today] = conversation_history
        with open("progress.json", "w") as f:
            json.dump(progress, f)
        print("Progress saved. See you tomorrow.")
        break

    conversation_history.append({"role": "user", "content": user_input})

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation_history
    )

    reply = response.choices[0].message.content

    #handle the search
    if "SEARCH:" in reply:
        query = reply.split("SEARCH: ")[-1].strip()
        print(f"Searching for: {query}")
        results = tavily_client.search(query)
        context = results["results"][0]["content"]

        conversation_history.append({"role": "assistant", "content": reply})
        conversation_history.append({"role":"user", "content":f"Search results: {context}"})

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation_history
        )

        reply = response.choices[0].message.content

    conversation_history.append({"role": "assistant", "content": reply})
    print(f"\nCoach: {reply}\n") 