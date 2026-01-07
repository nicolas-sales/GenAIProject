# GenAI RAG Assistant


## Overview

This project is a **Retrieval-Augmented Generation (RAG) assistant** designed to answer technical questions about **Generative AI, RAG, LangChain, and Hugging Face** using a curated set of documents.

The assistant relies exclusively on retrieved documents (PDFs and static web pages) and does not hallucinate answers outside its knowledge base.  
If the information is not present in the indexed documents, the assistant explicitly responds that it does not know.

The project is built as a learning and portfolio project, with a clean and extensible architecture that can evolve toward production-ready systems.

---

## Objectives

- Learn and apply RAG concepts end-to-end
- Use LangChain for orchestration
- Use OpenAI models for embeddings and generation
- Build a modular, production-oriented architecture
- Separate concerns: ingestion, transformation, indexing, retrieval, generation
- Prepare the system for API and frontend integration

---

## Data Sources

The knowledge base is built from **static sources only**:

- PDF documents (GenAI courses, RAG books, institutional reports)
- Technical documentation pages
- Educational articles (scraped once, no live web access)

No live web search is performed at inference time.

---

## RAG Architecture

### High-level flow

- Documents are ingested from PDFs and web pages
- Text is cleaned and filtered
- Documents are chunked into overlapping segments
- Chunks are embedded using OpenAI embeddings
- Embeddings are stored in a Chroma vector database

At query time:

- Relevant chunks are retrieved using cosine similarity with MMR
- Retrieved context is injected into the prompt
- The LLM generates an answer strictly from the provided context

---

## Key Design Choices

### Retrieval

- Vector similarity search using cosine similarity
- MMR (Max Marginal Relevance) to reduce redundancy
- Tunable `k` and `fetch_k` parameters

### Generation

- OpenAI chat models
- Zero-temperature generation for factual consistency
- Strict system prompt to prevent hallucinations

### No Memory

- No conversational memory is used
- Each question is treated independently
- This ensures reproducibility and factual grounding

---

## Project Structure


GenAIProject/
│
├── app.py                           # Streamlit prototype (early RAG validation)
│
├── api/
│   └── main.py                      # FastAPI application (RAG API)
│
├── frontend/
│   ├── package.json                 # Frontend dependencies
│   ├── public/
│   └── src/
│       ├── App.js                   # React UI (text + voice interaction)
│       └── index.js                 # React entry point
│
├── requirements.txt                 # Backend Python dependencies
├── README.md
├── .gitignore
│
├── data/
│   └── raw/
│       └── pdf/                     # Source PDF documents
│
├── src/
│   ├── __init__.py
│   │
│   ├── logger.py                    # Centralized logging
│   ├── exception.py                 # Custom exception handling
│   │
│   ├── components/
│   │   ├── loaders/
│   │   │   ├── pdf_loader.py        # PDF document loader
│   │   │   └── web_loader.py        # Web page loader
│   │   │
│   │   ├── transformers/
│   │   │   ├── cleaner.py           # Text cleaning and filtering
│   │   │   └── chunker.py           # Document chunking
│   │   │
│   │   ├── vectorstore.py           # Chroma vector store manager
│   │   ├── llm.py                   # LLM abstraction (OpenAI)
│   │   └── rag_engine.py            # Retrieval + generation logic
│   │
│   └── pipeline/
│       ├── ingestion.py             # PDF & web ingestion pipeline
│       ├── build_index.py           # Cleaning, chunking, embedding, indexing
│       └── rag.py                   # Query-time RAG pipeline
│
└── chroma_db/                       # Persisted vector database (local only)



---

## Pipelines

### IngestionPipeline

- Loads PDF and web documents
- Normalizes metadata (`source_type`, `source_name`, `source_id`)
- Returns a unified list of LangChain `Document` objects

### BuildIndexPipeline

- Cleans document text
- Filters empty or low-quality content
- Splits documents into chunks
- Generates embeddings
- Persists the vector store on disk

### RAGPipeline

- Loads the existing vector store
- Creates an MMR-based retriever
- Builds the RAG engine

Returns:
- The generated answer
- The list of source documents used

---

## Source Transparency

Each answer includes the list of source documents that contributed to the response.  
Duplicate sources are deduplicated at display time for clarity.

This makes the assistant suitable for educational and professional contexts where traceability is important.

---

## Deployment Notes

### Streamlit

- Streamlit was used successfully for local prototyping
- Streamlit Community Cloud was tested but abandoned due to limitations with native dependencies (PyMuPDF, Chroma)

---

---

## FastAPI Backend

The project is implemented as a **FastAPI backend** exposing the RAG system through a clean and well-defined API.

Key characteristics:

- The RAG logic is fully decoupled from any user interface
- The `RagPipeline` can be reused directly inside API endpoints
- Input and output schemas are validated using Pydantic
- The API returns both the generated answer and the list of source documents used
- No conversational memory is used, ensuring deterministic and reproducible answers

This design makes the backend suitable for integration with any client application (web, mobile, internal tools).


---

## Frontend Integration

A lightweight **React frontend** is provided as a demonstration interface.

The frontend allows users to:
- Ask questions using text input or voice dictation
- Receive grounded answers generated by the RAG system
- View the list of document sources used to generate each answer

The frontend is intentionally minimal and serves as a product-oriented showcase of the RAG system rather than a full UI application.


---

## Deployment Considerations

The project is currently designed for **local execution**.

No cloud deployment is required to validate the architecture or the RAG logic.  
The system can be deployed to a cloud provider (e.g. AWS, GCP, or Azure) if needed, but deployment is considered an infrastructure concern and is intentionally kept out of scope for this project.

The focus of this project is on:
- Retrieval-Augmented Generation design
- Robust document grounding
- Clean software architecture
- Reproducible and explainable outputs


---

## Project Status

- End-to-end RAG pipeline implemented and functional
- PDF and web document ingestion validated
- Text cleaning and chunking implemented
- Vector store indexing completed
- MMR-based retrieval validated
- Source attribution implemented
- FastAPI backend operational
- Frontend successfully integrated

The project is considered **complete and production-ready at the architectural level**, and can serve as a solid foundation for further extensions such as agents, streaming responses, or cloud deployment.
