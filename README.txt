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
│   ├── vectorstore.py           # class VectorStoreManager
│   ├── llm.py                   # class LLMProvider
│   └── rag_engine.py            # class RAGEngine
│
├── pipeline/
│   ├── ingestion.py             # class IngestionPipeline
│   ├── build_index.py           # class IndexPipeline
│   └── rag.py                   # class RAGPipeline




Note: This project uses LangChain 0.2.x for stability.
Chroma deprecation warnings are expected and safe.
