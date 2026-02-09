from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
from typing import List

def load_policy_pdf(pdf_path : str) -> List[Document]:
    """
    Loads the policy PDF and returns a list of LangChain Document objects.
    Each Document corresponds to one page.
    """
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    return documents