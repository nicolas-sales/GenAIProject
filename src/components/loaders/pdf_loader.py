from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path


class PdfLoader:

    def __init__(self,pdf_path:Path):
        if not isinstance(pdf_path, Path):
            raise TypeError("pdf_path must be a pathlib.Path")
        
        self.pdf_path=pdf_path

    
    def load(self):
        loader = PyPDFLoader(str(self.pdf_path))
        docs = loader.load()

        for doc in docs:
            doc.metadata["source_type"] = "pdf"
            doc.metadata["source_name"] = self.pdf_path.name
            doc.metadata["source_id"] = self.pdf_path.name

        return docs
