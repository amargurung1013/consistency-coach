from langchain_community.document_loaders import TextLoader
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv(override=True)

#load_docs
loader = TextLoader("data.txt")
docs = loader.load()

#split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size =500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

#embed and store
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(chunks, embeddings)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Answer the question using only the context below.\n\nContext: {context}"),
        ("user", "{question}")
    ]
)

def format_docs(docs):
    return "\n".join(doc.page_content for doc in docs)

#build retriver
retriever = vectorstore.as_retriever()

#build chain
llm = ChatGroq(model="llama-3.3-70b-versatile")
chain = (
    {"context": retriever | format_docs, "question" : RunnablePassthrough()} | prompt | llm | StrOutputParser()
)

#printing result
result = chain.invoke("Which plant has the most moons?")
print(result)