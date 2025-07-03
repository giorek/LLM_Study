import os
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS
import pickle

def test_faiss():
    embedding = DashScopeEmbeddings(
        model="text-embedding-v4",
        dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"),
    )
    text = "Hello, world!"
    knowledgeBase = FAISS.from_texts([text], embedding)
    knowledgeBase.save_local(os.path.join(os.path.dirname(__file__), "faiss_index"))

def read_faiss():
    embedding = DashScopeEmbeddings(
        model="text-embedding-v4",
        dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"),
    )
    knowledgeBase = FAISS.load_local(
        os.path.join(os.path.dirname(__file__), "faiss_index"),
        embedding,
        allow_dangerous_deserialization=True
    )
    print(knowledgeBase.similarity_search("Hello, world!"))
    return knowledgeBase


if __name__ == "__main__":
    #test_faiss()
    read_faiss()