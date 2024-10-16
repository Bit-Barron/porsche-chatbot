from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
import os

os.environ["OPENAI_API_KEY"] = "gsk_djTBAsSylkPQyWh3YmnaEWGdyb3FYfTwvuUjA6uHKiLrou2rtHClo"

loader = TextLoader("connect_output.txt")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
db = Chroma.from_documents(texts, embeddings)

retriever = db.as_retriever()
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)

query = "How do I add a vehicle to my Porsche ID profile?"
result = qa({"query": query})
print(result["result"])

