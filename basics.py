from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(override=True)

llm = ChatGroq(model="llama-3.3-70b-versatile")
parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that explains things simply!"),
        ("user", "{input}")
    ]
)
chain = prompt | llm | parser

response = chain.invoke({"input": "What is RAG in one sentence?"})

print(response)