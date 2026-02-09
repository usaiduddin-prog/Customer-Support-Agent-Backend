from rag.loader import load_policy_pdf
from rag.splitter import split_policy_documents
from rag.embeddings import build_faiss_index

PDF_PATH = "data/policy_pdf.pdf"

docs = load_policy_pdf(PDF_PATH)
chunks = split_policy_documents(docs)

vectorstore = build_faiss_index(chunks)

print(f"FAISS index built with {len(chunks)} chunks.")