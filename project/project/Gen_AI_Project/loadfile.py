from datetime import datetime
from chroma import add_file,get_data_for_Embed_query
from embedding import create_embedding
import streamlit as st



def chunk_file_data(documents):
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200,
                                                 separators=["\n\n"]
        )
    docs=text_splitter.create_documents(documents)

    gernerate_metadata(docs)
    print("Chunking Done...")
    st.write("File Processed Successfully...")

def gernerate_metadata(docs):
    for i, doc in enumerate(docs):
        lines = doc.page_content.split("\n")
        title = ""
        for line in lines:
            line = line.strip()
            if line.startswith("Title:"):
                title = line.replace("Title:", "").strip()
                break
        if not title:
            title = f"Uploaded File - Part {i+1}"

        metadata = {"source": f"Uploaded File-{datetime.now()} - Part {i+1}", "title": title}
        id = f"Uploaded_File_{i+1}"
        emb = create_embedding(doc.page_content)
  
        add_file(ids=[id], vectordb=emb, metadata=[metadata], doc=[doc.page_content])

def get_data_from_file(query: str) -> str:
    try:
        embedding = create_embedding([query])
        result = get_data_for_Embed_query(embedding, option="file")
        return str(result["documents"])
    except Exception as e:
        return f"An error occurred: {e}"