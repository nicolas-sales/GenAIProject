from langchain_core.prompts import ChatPromptTemplate


class RagEngine:

    def __init__(self,retriever,llm):
        self.retriever=retriever
        self.llm=llm

        # Prompt RAG
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                "You are an expert AI Engineer."
                "Answer the question using only the provided context."
                "If the answer is not in the cintzxt, say 'I don't know'."
                ),
                (
                "user",
                "CONTEXT:\n{context}\n\nQUESTION:\n{question}"
                )
            ]
        )

    def answer(self,question: str) -> str:
        # Retrieval
        docs = self.retriever.invoke(question) # retriever interroge chroma, il retourne une liste de documents
                                               # Chaque document contient : page_content (texte) et metadata (source, pdf/web)

        # Context
        context = "\n\n".join(doc.page_content for doc in docs) # Concaténation brute des chunks récupérés, séparés par des sauts de ligne

        # Chain (Prompt+LLM)
        chain = self.prompt | self.llm

        response = chain.invoke( # Appel de la chain
            {
                "context":context,
                "question":question # rag_prompt reçoit le context et la question. Un prompt final est généré et est envoyé au llm OpenAI
            }
        )

        return {
            "answer":response.content,
            "sources":docs
        }