from sentence_transformers import SentenceTransformer
from app.core.logger import logger
from typing import List

class Embedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        logger.info(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        logger.info("Embedding model loaded successfully.")

    def embed_text(self, text: str) -> List[float]:
        """Converts a single string into a vector."""
        embedding = self.model.encode(text)
        return embedding.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Converts a list of strings into a list of vectors."""
        embeddings = self.model.encode(texts)
        return embeddings.tolist()


embedder = Embedder()
