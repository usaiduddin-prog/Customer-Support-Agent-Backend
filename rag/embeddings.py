from typing import List
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def build_faiss_index(
    documents: List[Document],
    index_path: str = "rag/faiss_index"
) -> FAISS:
    """
    Builds and saves a FAISS vector store from policy document chunks.
    """

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(
        documents=documents,
        embedding=embedding_model
    )

    vectorstore.save_local(index_path)

    return vectorstore