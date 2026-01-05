from pathlib import Path
import sys

from src.logger import logger
from src.exception import CustomException

from src.pipeline.ingestion import IngestionPipeline
from src.components.transformers.cleaner import TextCleaner
from src.components.transformers.chunker import TextChunker
from src.components.vectorstore import VectorStoreManager


class BuildIndexPipeline:
    def __init__(self,pdf_dir: Path,urls: list[str],persist_directory : str ="./chroma_db",collection_name: str = "genai_docs",embedding_model: str = "text-embedding-3-small"):
        self.pdf_dir=pdf_dir
        self.urls=urls
        self.persist_directory=persist_directory

        # Components
        self.cleaner=TextCleaner(min_length=80)
        self.chunker=TextChunker(chunk_size=1000,chunk_overlap=150)
        self.vectorstore=VectorStoreManager(
            persist_directory=persist_directory,
            collection_name=collection_name,
            embedding_model=embedding_model,
        )

    def run(self):
        try:
            logger.info("Starting BuildIndexPipeline")

            # Ingestion
            ingestion=IngestionPipeline(pdf_dir=self.pdf_dir,urls=self.urls)
            documents=ingestion.run()
            logger.info(f"Ingested {len(documents)} raw documents")

            # Cleaning
            documents=self.cleaner.filter(documents)
            logger.info(f"{len(documents)} documents after cleaning")

            # Chunking
            chunks=self.chunker.chunk(documents)
            logger.info(f"{len(chunks)} chunks created")

            # Vector store build
            self.vectorstore.build(chunks)
            logger.info("Vector store built")

        except Exception as e:
            logger.error("Error during BuildIndexPipeline")
            raise CustomException(e,sys)
        

if __name__=="__main__":

    project_root = Path(__file__).resolve().parents[2] 
        # parent[0] -> pipeline; parent[1] -> src; parent[2] -> GenAIProject
        #  __file__ pointe vers ingestion.py

    pdf_dir = project_root / "data" / "raw" / "pdf"

    urls = ["https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/overview?utm_source=chatgpt.com&hl=fr"]

    pipeline = BuildIndexPipeline(
        pdf_dir=pdf_dir,urls=urls,persist_directory="./chroma_db",collection_name="genai_docs",embedding_model="text-embedding-3-small"
    )

    pipeline.run()

    print("BuildIndexPipeline run perfectly!")