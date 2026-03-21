import streamlit as st
from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv(override=True)

st.title("🎥 YouTube Video Chat")
st.write("Paste any YouTube URL and chat with the video content.")

video_url = st.text_input("YouTube URL")

if video_url:
    with st.spinner("Loading video transcript..."):
        loader = YoutubeLoader.from_youtube_url(video_url, add_video_info=False)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma.from_documents(chunks, embeddings)
        retriever = vectorstore.as_retriever()
        llm = ChatGroq(model="llama-3.3-70b-versatile")

        def format_docs(docs):
            return "\n".join(doc.page_content for doc in docs)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Answer using only the video transcript context below.\n\nContext: {context}"),
            ("user", "{question}")
        ])

        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    st.success("Video loaded! Ask anything about it.")

    question = st.text_input("Your question")

    if question:
        with st.spinner("Thinking..."):
            result = chain.invoke(question)
        st.write(f"**Answer:** {result}")
