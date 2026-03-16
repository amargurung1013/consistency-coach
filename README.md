# Consistency Coach 🎯

A personal AI accountability coach that knows your goals, tracks your 
daily progress, and keeps you on track — built with raw Python, no frameworks.

## What it does
- Checks in on you daily and tracks what you completed
- Remembers your goals and progress across sessions
- Warns you as exam dates approach
- Searches for resources when you're stuck
- Calls you out when you're slipping

## My goals it tracks
- Build one AI project every day
- Learn one new AI concept every day
- Master LangChain and LangGraph
- Exam prep for 7 subjects (April 7th)

## How it works
1. Loads your goals and past progress on startup
2. Injects everything into the agent's memory
3. You chat with your coach naturally
4. On exit, saves the full conversation to progress.json
5. Next session it remembers everything

## Stack
- Python
- Groq (LLaMA 3.3) — the brain
- Tavily — web search for resources
- JSON — goal and progress storage

## Built as part of my AI Agents learning journey
RAG → Tool Calling → Memory → Agent Loop → This project

## Setup
1. Clone the repo
2. Add your API keys to .env
3. Fill in your goals in goals.json
4. Run: uv run coach.py
```

