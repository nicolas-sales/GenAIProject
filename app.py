import streamlit as st

from src.pipeline.rag import RagPipeline

# Config
st.set_page_config(
    page_title="GenAI RAG Assistant",
    layout="centered"
)

st.title("GenAI RAG Assistant")
st.write("Ask technical questions about GenAI, Rag, Langchain, Hugging Face")

# Initialisation pipeline

def load_rag_pipeline():
    return RagPipeline(
        persist_directory="./chroma_db",collection_name="genai_docs",embedding_model="text-embedding-3-small",
        llm_model="gpt-4.1-mini",temperature=0.0,
        search_type="mmr",k=5,fetch_k=20
    )

rag_pipeline=load_rag_pipeline()

# User input

question=st.text_input(
    "Your question",
    placeholder="What is Retrieval-Augmented Generation?"
)

# Button

if st.button("Ask"):
    if question.strip()=="":
        st.warning("Please enter a question")
    else:
        with st.spinner("Thinking..."):
            result=rag_pipeline.run(question)

        st.subheader("Answer")
        st.write(result["answer"])

        st.subheader("Sources")

        # Affichage de la source en évitant les doublons

        seen = set() # Création ensemble vide (mémoire temporaire)
        for doc in result["sources"]: # Pour chaque chunk
            source_name = doc.metadata.get("source_name", "unknown") # .get() évite une erreur si la clé n'existe pas, récupération de ce qui a été défini à l'ingestion
            source_type = doc.metadata.get("source_type", "unknown")

            key = (source_name, source_type) # tuple, exemple : ("gen-ai-handbook-fr.pdf", "pdf") -> source unique
            if key in seen:
                continue # Si la source est déjà dans seen, on saute ce chunk, la source n'est donc pas affichée deux fois
            seen.add(key)

            st.markdown(f"- **{source_type.upper()}** — {source_name}")