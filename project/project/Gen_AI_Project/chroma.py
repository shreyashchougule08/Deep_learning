import chromadb


db1 = chromadb.PersistentClient(path="./Uploaded_file")
content_file = db1.get_or_create_collection("File_Uploaded")

db = chromadb.PersistentClient(path="./Sunbeam_data")
content_scraping = db.get_or_create_collection("Sunbeam_web_data")

def add_file(ids,vectordb,metadata,doc):
    try:
        db1 = chromadb.PersistentClient(path="./Uploaded_file")
        content_file = db1.get_or_create_collection("File_Uploaded")
        content_file.add(ids=ids,embeddings=vectordb,metadatas=metadata,documents=doc)
        return "file added"
    except Exception:
        return "failed to Add Data"
    
def add_sunbeam_data(ids,vectordb,metadata,doc):
    content_scraping.add(ids=ids,embeddings=vectordb,metadatas=metadata,documents=doc)
    return "Scrapping Done"

def delete_data(id,options="file"):
    if options=="file":
        try :
            content_file.delete(ids=[id])
            return "deleted successfully"
        except Exception :
            return "failed to Detete"
    else:
        try :
            content_scraping.delete(ids=[id])
            return "deleted successfully"
        except Exception :
            return "failed to Detete"

def update_data(id,vectordb,metadata,option="file"):
    if option=="file":
        try:
            delete_data(id,option)
            content_file.add(ids=id,embeddings=vectordb,metadatas=metadata)
            return "Updated Sucessfully.."
        except Exception :
            return "Failed to Update.."
    else:
        try:
            delete_data(id,option)
            content_scraping.add(ids=id,embeddings=vectordb,metadatas=metadata)
            return "Updated Sucessfully.."
        except Exception :
            return "Failed to Update.."


def get_data_for_Embed_query(Equery,option="sunbeam"):
    if option=="file":
        result=content_file.query(query_embeddings=Equery,n_results=3,)
    else:
        result=content_scraping.query(query_embeddings=Equery,n_results=3,)
    return result

if __name__=="__main__":
    from embedding import create_embedding
    while True:
        data=input("Enter data to be embedded : ")
        emb=create_embedding([data])
        print("Embedding : ",emb)
        res=get_data_for_Embed_query(emb,option="sunbeam")
        print("Result : ",res["documents"])