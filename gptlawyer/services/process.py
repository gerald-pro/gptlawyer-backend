import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone as vector_picone

class SPinecone:
    embeddings = OpenAIEmbeddings()
    # Configurar el divisor de texto
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    @classmethod
    def create_index(cls,name_index):
        if name_index not in cls.pc.list_indexes().names():
            print(f"El indice {name_index} no existe")
            print("Creando el indice ...")
            cls.pc.create_index(name_index,dimension=1536,
                        metric="cosine",
                        spec=ServerlessSpec(
                            cloud="aws",
                            region="us-east-1"
                        ))
        else:
            print(f"El indice {name_index} ya existe en Pinecone" )
    @classmethod
    def delete_index(cls,name_index):
        if name_index in cls.pc.list_indexes().names():
            print(f"Eliminando el indice {name_index} ...")
            cls.pc.delete_index(name_index)
        else:
            print(f"El indice {name_index} no existe en Pinecone" )

    @classmethod
    def txtToEmbedding(cls,index_name,text):
        texts = cls.divide_text(text)
        print("Cantidad de vectores: "+str(len(texts)) )
        vector_picone.from_texts([t.page_content for t in texts],cls.embeddings, index_name=index_name)

    @classmethod
    def divide_text(cls,text):
        texts = cls.text_splitter.create_documents([text])
        return texts


    
#SPinecone.txtToEmbedding("caso-16","hola gracias gente")
