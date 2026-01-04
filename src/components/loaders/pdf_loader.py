from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path

def load_pdf(pdf_path: Path):
    loader = PyPDFLoader(str(pdf_path))
    docs = loader.load()

    for doc in docs:
        doc.metadata["source_type"] = "pdf"
        doc.metadata["source_name"] = pdf_path.name
        doc.metadata["source_id"] = pdf_path.name

    return docs
