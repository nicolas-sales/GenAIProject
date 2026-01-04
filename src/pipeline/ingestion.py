from pathlib import Path
import sys

from src.logger import logger
from src.exception import CustomException

from src.components.loaders.pdf_loader import PdfLoader
from src.components.loaders.web_loader import WebLoader


class IngestionPipeline:

    def __init__(self,pdf_dir: Path,urls: list[str]):
        self.pdf_dir=pdf_dir
        self.urls=urls

    def run(self):

        try:
            documents = []

            # PDF Ingestion

            logger.info(f"Starting PDF ingestion from: {self.pdf_dir}")

            pdf_files = [p for p in self.pdf_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"]
            # iterdir() : liste tout ce qu'il y a dans le dossier pdf_dir et renvoie une suite de Path
            # p for p in : On prend chaque élément (Path) du dossier, un par un
            # if p.is_file() :  si c'est bien un fichier
            # p.suffix : extension du fichier mis en minuscule (.pdf) pour que seuls les fichier pdf soient sélectionnés

            for pdf in pdf_files:
                logger.info(f"Loading PDF: {pdf.name}")
                loader=PdfLoader(pdf)
                documents.extend(loader.load())

                logger.info(f"PDF ingestion completed. Total PDF documents: {len(documents)}")

            # Web Ingestion

            logger.info(f"Staring Web ingestion for {len(self.urls)} URLS")

            web_loader = WebLoader(self.urls)
            documents.extend(web_loader.load())

            logger.info(f"Web ingestion completed. Total Web documents: {len(documents)}")

            logger.info(f"Total documents ingested: {len(documents)}")
            return documents
        
        except Exception as e:
            logger.error("Error occured during data ingestion")
            raise CustomException(e,sys)
        

if __name__=="__main__":

    project_root = Path(__file__).resolve().parents[2] 
        # parent[0] -> pipeline; parent[1] -> src; parent[2] -> GenAIProject
        #  __file__ pointe vers ingestion.py

    pdf_dir = project_root / "data" / "raw" / "pdf"

    urls = ["https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/overview?utm_source=chatgpt.com&hl=fr"]

    pipeline = IngestionPipeline(pdf_dir,urls)

    docs = pipeline.run()

    print(f"Total documents ingested: {len(docs)}")
    print(docs[0].metadata)
