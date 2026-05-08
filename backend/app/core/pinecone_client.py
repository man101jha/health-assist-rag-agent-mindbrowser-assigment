from pinecone import Pinecone,ServerlessSpec
from app.core.config import get_settings
from app.core.logger import logger
import time

settings = get_settings()

class PineconeManager:
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index_name = settings.PINECONE_INDEX_NAME
        self._initialize_index()
    def _initialize_index(self):
        """Ensures the index exists or creates it if missing."""
        try:
            # 1. Get list of existing indexes
            existing_indexes = [idx.name for idx in self.pc.list_indexes()]
            # 2. Create index if it doesn't exist
            if self.index_name not in existing_indexes:
                logger.info(f"Index {self.index_name} not found. Creating new index...")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=384, # Matching 'all-MiniLM-L6-v2'
                    metric='cosine',
                    spec=ServerlessSpec(cloud='aws', region='us-east-1')
                )
                # Wait for index to be initialized
                while not self.pc.describe_index(self.index_name).status['ready']:
                    time.sleep(1)
                logger.info(f"Index {self.index_name} created successfully.")
            
            self.index = self.pc.Index(self.index_name)
            logger.info(f"Pinecone Index '{self.index_name}' is ready.")
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {str(e)}")
            raise e



    def get_index(self):
        """Returns the Pinecone index instance."""
        return self.index

    def check_health(self):
        """Checks if the index is reachable."""
        try:
            stats = self.index.describe_index_stats()
            logger.info(f"Connected to Pinecone index: {self.index_name}")
            return True
        except Exception as e:
            logger.error(f"Pinecone health check failed: {str(e)}")
            return False

# Initialize the manager
pinecone_manager = PineconeManager()
