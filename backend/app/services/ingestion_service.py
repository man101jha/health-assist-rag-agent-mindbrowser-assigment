import os
from app.core.chunker import chunker
from app.core.embedder import embedder
from app.core.pinecone_client import pinecone_manager
from app.core.logger import logger

class IngestionService:
    def __init__(self):
        self.index = pinecone_manager.get_index()
        # This goes up from services/ to app/ to backend/ and then into data/
        self.data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
        
        logger.info(f"Looking for documents in: {self.data_path}")
        logger.info(f"Data folder exists: {os.path.exists(self.data_path)}")
        
    def ingest_all_documents(self):
        """Walks through the data folder and ingests every .txt file."""
        total_upserted = 0
        
        for root, dirs, files in os.walk(self.data_path):
            for file in files:
                if file.endswith(".txt") and file != "test_questions.txt":
                    file_path = os.path.join(root, file)
                    total_upserted += self._process_file(file_path, file)
        
        return total_upserted

    def _process_file(self, file_path: str, file_name: str):
        logger.info(f"Processing file: {file_name}")
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # 1. Chunking
        chunks = chunker.split_text(text)
        
        # 2. Embedding & Metadata Preparation
        vectors = []
        for i, chunk in enumerate(chunks):
            embedding = embedder.embed_text(chunk)
            vectors.append({
                "id": f"{file_name}_{i}",
                "values": embedding,
                "metadata": {
                    "source": file_name,
                    "text": chunk
                }
            })

        # 3. Batch Upsert to Pinecone
        self.index.upsert(vectors=vectors)
        logger.info(f"Successfully upserted {len(vectors)} vectors for {file_name}")
        return len(vectors)

ingestion_service = IngestionService()
