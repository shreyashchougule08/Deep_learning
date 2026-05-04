from langchain.embeddings import init_embeddings
from langchain_community.document_loaders import PyPDFLoader
from datetime import date
from chroma import *

embedding_model=init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5@q8_0",
    provider="openai" ,
    base_url="http://127.0.0.1:1234/v1",
    api_key="demo",
    check_embedding_ctx_length=False
    
)

def create_embedding(Data):
    emb=embedding_model.embed_documents(Data)
    print("Embedding Created...")
    return emb


if __name__=="__main__":
    md=create_embedding("Hello World")
    print(md)