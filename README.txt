# GenAI RAG Assistant

## Overview

This project is a Retrieval-Augmented Generation (RAG) assistant designed to answer technical questions about Generative AI, RAG, LangChain, and Hugging Face using a curated set of documents.

The assistant relies exclusively on retrieved documents (PDFs and static web pages) and does not hallucinate answers outside its knowledge base. If the information is not present in the indexed documents, the assistant explicitly responds that it does not know.

The project is built as a learning and portfolio project, with a clean and extensible architecture that can evolve toward production-ready systems.


## Objectives

Learn and apply RAG concepts end-to-end

Use LangChain for orchestration

Use OpenAI models for embeddings and generation

Build a modular, production-oriented architecture

Separate concerns: ingestion, transformation, indexing, retrieval, generation

Prepare the system for API and frontend integration


## Data Sources

The knowledge base is built from static sources only:

PDF documents (GenAI courses, RAG books, institutional reports)

Technical documentation pages

Educational articles (scraped once, no live web access)

No live web search is performed at inference time.


## RAG Architecture

### High-level flow 

Documents are ingested from PDFs and web pages

Text is cleaned and filtered

Documents are chunked into overlapping segments

Chunks are embedded using OpenAI embeddings

Embeddings are stored in a Chroma vector database

At query time:

Relevant chunks are retrieved using cosine similarity with MMR

Retrieved context is injected into the prompt

The LLM generates an answer strictly from the provided context


## Key Design Choices

### Retrieval

Vector similarity search using cosine similarity

MMR (Max Marginal Relevance) to reduce redundancy

Tunable k and fetch_k parameters

### Generation

OpenAI chat models

Zero-temperature generation for factual consistency

Strict system prompt to prevent hallucinations

### No Memory

No conversational memory is used

Each question is treated independently

This ensures reproducibility and factual grounding


## Project Structure:


GenAIProject/
│
├── app.py                         # Local Streamlit app (used for prototyping)
├── requirements.txt               # Pinned dependencies
├── README.md
├── .gitignore
│
├── data/
│   └── raw/
│       └── pdf/                   # Source PDF documents
│
├── src/
│   ├── __init__.py
│   │
│   ├── logger.py                  # Centralized logging
│   ├── exception.py               # Custom exception handling
│   │
│   ├── components/
│   │   ├── loaders/
│   │   │   ├── pdf_loader.py      # PDF ingestion
│   │   │   └── web_loader.py      # Web page ingestion
│   │   │
│   │   ├── transformers/
│   │   │   ├── cleaner.py         # Text cleaning and filtering
│   │   │   └── chunker.py         # Text chunking
│   │   │
│   │   ├── vectorstore.py         # Chroma vector store management
│   │   ├── llm.py                 # LLM provider abstraction
│   │   └── rag_engine.py          # Retrieval + generation logic
│   │
│   └── pipeline/
│       ├── ingestion.py           # Document ingestion pipeline
│       ├── build_index.py         # Cleaning, chunking, embedding, indexing
│       └── rag.py                 # Query-time RAG pipeline
│
└── chroma_db/                     # Vector database (local only, not versioned)



## Pipelines

### IngestionPipeline

Loads PDF and web documents

Normalizes metadata (source_type, source_name, source_id)

Returns a unified list of LangChain Document objects

### BuildIndexPipeline

Cleans document text

Filters empty or low-quality content

Splits documents into chunks

Generates embeddings

Persists the vector store on disk

### RAGPipeline

Loads the existing vector store

Creates an MMR-based retriever

Builds the RAG engine

Returns:

The generated answer

The list of source documents used


## Source Transparency

Each answer includes the list of source documents that contributed to the response. Duplicate sources are deduplicated at display time for clarity.

This makes the assistant suitable for educational and professional contexts where traceability is important.


## Deployment Notes

Streamlit

Streamlit was used successfully for local prototyping

Streamlit Community Cloud was tested but abandoned due to limitations with native dependencies (PyMuPDF, Chroma)


## FastAPI (Next Step)

The project is designed to be deployed as a FastAPI backend:

The RAG logic is already decoupled from the UI

RAGPipeline can be reused directly in an API endpoint

A React frontend can later consume the API
