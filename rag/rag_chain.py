from rag.retriever import load_retriever
from rag.generator import get_llm
from rag.prompts import RAG_PROMPT
from langchain.schema import Document

def format_docs(docs: list[Document]) -> str:
    return "\n\n".join(
        f"(Page {doc.metadata.get('page')}): {doc.page_content}"
        for doc in docs
    )

def get_rag_chain():
    retriever = load_retriever()
    llm = get_llm()

    def rag_pipeline(question: str):
        docs = retriever.invoke(question)
        context = format_docs(docs)

        chain = RAG_PROMPT | llm
        response = chain.invoke({
            "context": context,
            "question": question
        })

        return response.content, docs

    return rag_pipeline