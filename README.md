# 🎥 YouTube Video Chat
Chat with any YouTube video using AI.
Paste a URL, ask questions, get answers — no need to watch the full video.

## What it does
- Paste any YouTube URL
- Automatically loads the video transcript
- Ask anything about the video content
- Get accurate answers powered by RAG

## How it works
1. YoutubeLoader fetches the transcript
2. RecursiveCharacterTextSplitter chunks it
3. HuggingFaceEmbeddings embeds the chunks
4. ChromaDB stores the embeddings
5. User asks a question → relevant chunks retrieved
6. Groq (LLaMA 3.3) generates the answer

## Stack
- Python
- Streamlit — UI
- LangChain — RAG pipeline
- ChromaDB — vector storage
- HuggingFace — embeddings
- Groq (LLaMA 3.3) — LLM

## Setup
1. Clone the repo
2. Install dependencies:
   uv add streamlit langchain-community langchain-text-splitters langchain-huggingface langchain-groq chromadb youtube-transcript-api python-dotenv
3. Create .env file:
   GROQ_API_KEY="your-key-here"
4. Run:
   uv run streamlit run youtube_app.py

## Part of my AI learning journey
Built during my LangChain learning phase after mastering
RAG, tool calling, memory, and agent loops from scratch.

Previous work: github.com/amargurung1013/rag-from-scratch
