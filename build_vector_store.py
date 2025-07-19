from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings


#from langchain.vectorstores import FAISS
#from langchain.embeddings import OpenAIEmbeddings
from load_documents import load_and_split
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def build_faiss_index(pdf_paths, index_path="faiss_index"):
    all_chunks = []
    for path in pdf_paths:
        chunks = load_and_split(path)
        all_chunks.extend(chunks)

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(index_path)
    print(f"Vector store saved to {index_path}")

if __name__ == "__main__":
    build_faiss_index(["privacy_policy.pdf", "terms_and_conditions.pdf"])
