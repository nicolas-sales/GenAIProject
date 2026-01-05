from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextChunker:
    def __init__(self,chunk_size: int =1000,chunk_overlap: int =150):
        self.chunk_size=chunk_size
        self.chunk_overlap=chunk_overlap

    def chunk(self,documents):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
            )   

        chunks = text_splitter.split_documents(documents)
    
        return chunks