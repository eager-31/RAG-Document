import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    USE_LOCAL_LLM: bool = os.getenv("USE_LOCAL_LLM", "false").lower() == "true"
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama3-8b-8192") # Default Groq model
    
    # Paths
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    RAW_DIR: str = os.path.join(DATA_DIR, "raw")
    PROCESSED_DIR: str = os.path.join(DATA_DIR, "processed")
    FAISS_INDEX_PATH: str = os.path.join(PROCESSED_DIR, "faiss_index")
    CHUNKS_JSON_PATH: str = os.path.join(PROCESSED_DIR, "chunks.json")
    DB_PATH: str = os.path.join(BASE_DIR, "storage", "rag_logs.db")
    
    # Chunking
    CHUNK_SIZE: int = 600
    CHUNK_OVERLAP: int = 100
    
    # Embedding
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Ensure directories exist
os.makedirs(settings.RAW_DIR, exist_ok=True)
os.makedirs(settings.PROCESSED_DIR, exist_ok=True)
os.makedirs(os.path.dirname(settings.DB_PATH), exist_ok=True)
