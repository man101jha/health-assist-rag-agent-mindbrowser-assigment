from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.logger import logger

class DocumentChunker:
    def __init__(self, chunk_size: int = 600, chunk_overlap: int = 80):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def split_text(self, text: str):
        """Splits a single document into chunks."""
        chunks = self.splitter.split_text(text)
        logger.info(f"Split document into {len(chunks)} chunks.")
        return chunks

# Singleton instance
chunker = DocumentChunker()
