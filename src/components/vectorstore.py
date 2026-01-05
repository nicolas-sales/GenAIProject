from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


class VectorStoreManager:
    def __init__(self,persist_directory : str ="./chroma_db",collection_name: str ="genai_docs",embedding_model: str = "text-embedding-3-small"):
        self.persist_directory=persist_directory
        self.collection_name=collection_name

        # Embedding OpenAI
        self.embeddings = OpenAIEmbeddings(model=embedding_model)

        # Vectoe store (initialisé plus tard)
        self.vectorstore = None

    def build(self,documents):

        self.vectorstore=Chroma.from_documents(documents=documents,embedding=self.embeddings,persist_directory=self.persist_directory,collection_name=self.collection_name)
        # collection = un index vectoriel logique dans Chroma

        self.vectorstore.persist() # # sauvegarde la base vectorielle sur le disque, permet de ne pas les garder qu'en mémoire car au redémarrage du notebook tout est perdu
        return self.vectorstore
    
    def load(self):
        """
        Load an existing persisted vector store
        """
        self.vectorstore=Chroma(embedding_function=self.embeddings,persist_directory=self.persist_directory,collection_name=self.collection_name)
        return self.vectorstore
    
    def as_retriever(self,search_type : str ="mmr",k :int =5,fetch_k: int =20):

        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Call build() or load()")
        
        return self.vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs={
                "k":k,
                "fetch_k":fetch_k}
        )