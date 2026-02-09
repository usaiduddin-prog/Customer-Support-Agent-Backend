from langchain_community.vectorstores import FAISS 
from langchain_huggingface import HuggingFaceEmbeddings

def load_retriever(
    index_path: str = "rag/faiss_index",
    k: int = 4
):
    """
    Loads FAISS index and returns a retriever.
    """

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.load_local(
        index_path,
        embedding_model,
        allow_dangerous_deserialization=True
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": k}
    )

    return retriever