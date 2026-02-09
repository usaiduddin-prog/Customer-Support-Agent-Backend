from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


def split_policy_documents(
    documents: List[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 80,
    toc_page_index: int = 1,
) -> List[Document]:
    """
    Splits policy PDF documents into chunks suitable for RAG.
    Excludes the Table of Contents page.
    """

    filtered_docs = [
        doc for doc in documents
        if doc.metadata.get("page") != toc_page_index
    ]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    chunks = splitter.split_documents(filtered_docs)

    final_chunks = []
    chunk_counter = {}

    for chunk in chunks:
        page = chunk.metadata.get("page", "unknown")

        if page not in chunk_counter:
            chunk_counter[page] = 0

        chunk_counter[page] += 1

        chunk.metadata["chunk_id"] = f"policy_p{page}_c{chunk_counter[page]}"

        final_chunks.append(chunk)

    return final_chunks