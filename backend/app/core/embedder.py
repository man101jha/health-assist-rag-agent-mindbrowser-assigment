from fastembed import TextEmbedding
from app.core.logger import logger

class Embedder:
    def __init__(self, model_name="BAAI/bge-small-en-v1.5"):
        logger.info(f"Initializing FastEmbed engine with model: {model_name}")
        try:
            self.model = TextEmbedding(model_name=model_name)
            logger.info("FastEmbed engine initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize FastEmbed: {e}")
            raise

    def embed_text(self, text: str) -> list:
        """Generate a single embedding vector for the given text."""
        try:
            # fastembed returns a generator of numpy arrays
            embeddings = list(self.model.embed([text]))
            return embeddings[0].tolist()
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise

# Singleton instance
embedder = Embedder()
