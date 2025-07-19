#from langchain.vectorstores import FAISS
#from langchain.embeddings import OpenAIEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def get_context(query, index_path="faiss_index", k=3):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    db = FAISS.load_local(index_path, embeddings)
    results = db.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in results])
