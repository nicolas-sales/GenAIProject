from pathlib import Path
import sys

from src.logger import logger
from src.exception import CustomException

from src.components.vectorstore import VectorStoreManager
from src.components.llm import LLMProvider
from src.components.rag_engine import RagEngine


class RagPipeline:

    def __init__(
            self,
            persist_directory : str ="./chroma_db",collection_name: str = "genai_docs",embedding_model: str = "text-embedding-3-small",
            llm_model: str ="gpt-4.1-mini",temperature : float =0.0,
            search_type : str ="mmr",k :int =5,fetch_k: int =20
    ):
        self.persist_directory=persist_directory
        self.collection_name=collection_name
        self.embedding_model=embedding_model
        self.search_type=search_type
        self.k=k
        self.fetch_k=fetch_k

        # Vector store (load)
        self.vectorstore = VectorStoreManager(
            persist_directory=self.persist_directory,
            collection_name=self.collection_name,
            embedding_model=self.embedding_model
        )

        # LLM
        self.llm=LLMProvider(
            model_name=llm_model,temperature=temperature
        ).get()

    def run(self,question: str) -> str:
        try:
            logger.info("Starting RagPipeline")

            # Load vector store
            self.vectorstore.load()

            # Retriever
            retriever=self.vectorstore.as_retriever(search_type="mmr",k=5,fetch_k=20)

            # RAG
            rag=RagEngine(retriever=retriever,llm=self.llm)

            # Answer
            answer=rag.answer(question)

            logger.info("RagPipeline completed successfully")
            return answer
        
        except Exception as e:
            logger.error("Error during RagPipeline")
            raise CustomException(e,sys)
        



if __name__=="__main__":
    pipeline=RagPipeline(
        persist_directory="./chroma_db",collection_name="genai_docs",embedding_model="text-embedding-3-small",
        llm_model="gpt-4.1-mini",temperature=0.0,
        search_type="mmr",k=5,fetch_k=20
    )

    question="What is RAG?"
    answer= pipeline.run(question)

    print("\nQUESTION:\n", question)
    print("\nANSWER:\n", answer)
