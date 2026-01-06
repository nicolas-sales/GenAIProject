from fastapi import FastAPI, HTTPException
from pydantic import BaseModel # définir des schémas JSON
from typing import List # typing Python

from src.pipeline.rag import RagPipeline

# Pydantic valide les données, transforme JSON en objets Python, empêche les erreurs, génère la doc API, rend le backend fiable

# Schema

class AskRequest(BaseModel): # Définit ce que le client doit envoyer
    question: str


class Source(BaseModel): # Représente une source unique (pdf ou web)
    source_type: str
    source_name: str


class AskResponse(BaseModel): # Décrit le format de réponse complet
    answer: str
    sources: List[Source]


# Initialization FastAPI + RAG

app = FastAPI(
    title="GenAI RAG API",
    description="RAG backend for GenAI assistant",
    version="1.0.0",
)

rag_pipeline = RagPipeline(
    persist_directory="./chroma_db",collection_name="genai_docs",embedding_model="text-embedding-3-small",
    llm_model="gpt-4.1-mini",temperature=0.0,
    search_type="mmr",k=5,fetch_k=20
)

# Quand quelqu’un fait une requête HTTP POST sur /ask, alors FastAPI appelle la fonction ask_question
@app.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest): # payload = JSON validé automatiquement

    if not payload.question.strip(): # .strip() enlève les espaces, empêche " " comme question
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    result = rag_pipeline.run(payload.question)

    # déduplication des sources
    seen = set()
    sources = []

    for doc in result["sources"]:
        source_type = doc.metadata.get("source_type", "unknown")
        source_name = doc.metadata.get("source_name", "unknown")

        key = (source_type, source_name)
        if key in seen:
            continue
        seen.add(key)

        sources.append(
            Source(
                source_type=source_type,
                source_name=source_name,
            )
        )

    return AskResponse(
        answer=result["answer"],
        sources=sources,
    )
