from pathlib import Path
import sys

from src.logger import logger
from src.exception import CustomException

from src.components.loaders.pdf_loader import load_pdf
from src.components.loaders.web_loader import load_web_pages

def ingest_documents(pdf_dir: Path, urls: list[str]):

    """
    Ingest PDF from directory and Web documents from URLS
    Return a list of Langchain documents
    """

    try:
        documents = []

        # PDF Ingestion

        if pdf_dir and pdf_dir.exists():
            logger.info(f"Starting PDF ingestion from: {pdf_dir}")

            pdf_files = [p for p in pdf_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"]

            for pdf in pdf_files:
                logger.info(f"Loading PDF: {pdf.name}")
                pdf_docs=load_pdf(pdf)
                documents.extend(pdf_docs)

            logger.info(f"PDF ingestion completed. Total PDF documents: {len(documents)}")

        # Web Ingestion

        if urls:
            logger.info(f"Staring Web ingestion for {len(urls)} URLS")
            web_docs = load_web_pages(urls)
            documents.extend(web_docs)
            logger.info(f"Web ingestion completed. Total Web documents: {len(documents)}")

        logger.info(f"Total documents ingested: {len(documents)}")
        return documents
    
    except Exception as e:
        logger.error("Error occured during data ingestion")
        raise CustomException(e,sys)
    

if __name__=="__main__":
    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2] 
    # parent[0] -> pipeline; parent[1] -> src; parent[2] -> GenAIProject
    #  __file__ pointe vers ingestion.py
    pdf_dir = project_root / "data" / "raw" / "pdf"

    urls = ["https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/overview?utm_source=chatgpt.com&hl=fr"]

    docs = ingest_documents(pdf_dir=pdf_dir,urls=urls)

    print(f"Total documents ingested: {len(docs)}")
    print(docs[0].metadata)
