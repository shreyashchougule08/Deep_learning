import re
import numpy as np
from scrapping.Add_data_to_file import get_all_data_from_file
from chroma import add_sunbeam_data, add_file
from embedding import create_embedding
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_sunbeam_data():
    data,text_courses=get_all_data_from_file()
    data = data.replace("ï¿½", "•")
    data = re.sub(r'\\', '', data)
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200,
                                                 separators=["#"]
        )
    
    text_splitter1=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200,
                                                 separators=["---"]
        )
    docs=text_splitter.create_documents([data])
    docs+=text_splitter1.create_documents([text_courses])
    # docs.extend(docs_courses)
    gernerate_metadata(docs)
   
    print("Chunking Done...")
    return docs



def gernerate_metadata(docs):
    for i, doc in enumerate(docs):
        lines = doc.page_content.split("\n")
        title = ""
        for line in lines:
            line = line.strip()
            if line.startswith("#"):
                title = line.replace("#", "").strip()
                break
            elif line.startswith("---"):
                title = line.replace("---", "").strip()
                break
        if not title:
            title = "Sunbeam Info"

        metadata = {"source": f"Sunbeam Info - Part {i+1}", "title": title}
        id = f"Sunbeam_Info_{i+1}"

        emb = create_embedding(doc.page_content)

        if isinstance(emb, list) and emb and isinstance(emb[0], (list, tuple)):
            vectordb = np.mean(np.asarray(emb, dtype=float), axis=0).tolist()
        else:
            vectordb = emb

        add_sunbeam_data(ids=[id], vectordb=[vectordb], metadata=[metadata], doc=[doc.page_content])

        # print("len -->",len(vectordb))
        # print("id -->",len(id))
        # print("metadata -->",len(metadata))



if __name__=="__main__":
    docs = chunk_sunbeam_data()
    print("len of docs :",len(docs))

    # with open("Chunk.txt",mode="a") as f:
    #         for doc in docs:
    #             f.write(str(doc.page_content))
    #             f.write("\n"+"*"*100+"\n")


# for doc in docs:
#     # print("****"*30)
#     print("\nChunk--> : ",doc)

                                                 