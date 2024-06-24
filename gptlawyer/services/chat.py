import os
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from pinecone import Pinecone
from langchain.vectorstores import Pinecone as VectorPinecone
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Cargar variables de entorno desde un archivo .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

class Chat:
    def __init__(self, index_name):
        self.pc = Pinecone(api_key=os.environ.get('PINECONE_API_KEY'))
        self.embed = OpenAIEmbeddings(model='text-embedding-ada-002', openai_api_key=os.getenv('OPENAI_API_KEY'))
        self.index = self.pc.Index(index_name) 
        self.vectorstore = VectorPinecone(self.index, self.embed.embed_query, "text")
        self.llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=1)
        self.retriever = self.vectorstore.as_retriever(search_type='similarity', search_kwargs={'k': 10})
        self.chain = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=self.retriever)
        self.text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=4,
        chunk_overlap=0,
        length_function=len
        )
    
    def query(self, text):
        return self.chain.run(text)