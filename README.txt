RAG project

src/
├── components/
│   ├── loaders/
│   │   ├── pdf_loader.py        # class PdfLoader
│   │   ├── web_loader.py        # class WebLoader
│   │
│   ├── transformers/
│   │   ├── cleaner.py           # class TextCleaner
│   │   ├── chunker.py           # class TextChunker
│   │
│   ├── embeddings.py            # class EmbeddingProvider
│   ├── vectorstore.py           # class VectorStoreManager
│   ├── retriever.py             # class RetrieverFactory
│   ├── llm.py                   # class LLMProvider
│   └── rag_engine.py            # class RAGEngine
│
├── pipeline/
│   ├── ingestion.py             # class IngestionPipeline
│   ├── build_index.py           # class IndexPipeline
│   └── rag.py                   # class RAGPipeline
