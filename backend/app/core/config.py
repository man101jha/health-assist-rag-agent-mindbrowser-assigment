from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # API Keys
    GROQ_API_KEY: str
    PINECONE_API_KEY: str
    
    # Config
    LLM_MODEL: str = "llama-3.1-8b-instant"
    PINECONE_INDEX_NAME: str = "health-assistant"
    
    # App Settings
    APP_NAME: str = "Healthcare AI Assistant"
    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings():
    return Settings()
