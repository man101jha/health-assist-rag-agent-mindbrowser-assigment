from groq import Groq
from app.core.embedder import embedder
from app.core.config import get_settings
from app.core.pinecone_client import pinecone_manager
from app.core.prompt import RAG_SYSTEM_PROMPT
from app.core.logger import logger

settings = get_settings()

class RAGService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.index = pinecone_manager.get_index()

    async def answer_question(self, query: str):
        # 1. Embed the user's question using shared embedder
        query_vector = embedder.embed_text(query)

        # 2. Search Pinecone for top 5 matches
        results = self.index.query(
            vector=query_vector,
            top_k=5,
            include_metadata=True
        )

        # 3. Extract context and sources
        context_chunks = []
        sources = []
        scores = []

        for match in results['matches']:
            context_chunks.append(match['metadata']['text'])
            sources.append({
                "document": match['metadata']['source'],
                "chunk": match['metadata']['text']
            })
            scores.append(match['score'])

        context_text = "\n\n---\n\n".join(context_chunks)

        # 4. Generate Answer using Groq
        response = self.client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[{"role": "user", "content": RAG_SYSTEM_PROMPT.format(context=context_text, question=query)}],
            temperature=0
        )

        # 5. Determine Confidence & Guardrails
        answer = response.choices[0].message.content
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # If AI apologizes (out of scope) or similarity is too low, hide sources
        is_refusal = "apologize" in answer.lower() or "don't have information" in answer.lower()
        
        if is_refusal or avg_score < 0.5:
            sources = []
            confidence = "low"
        else:
            confidence = "high" if avg_score > 0.8 else "medium" if avg_score > 0.6 else "low"

        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence
        }

rag_service = RAGService()
