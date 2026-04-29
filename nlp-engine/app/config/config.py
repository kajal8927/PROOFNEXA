import os
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = "ProofNexa NLP Engine"
    VERSION: str = "1.0.0"
    
    # Security
    ALLOWED_ORIGINS: List[str] = Field(
        default_factory=lambda: os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    )
    MAX_TEXT_LENGTH: int = Field(default=100000) # Limit text size to 100k chars
    RATE_LIMIT_PER_MINUTE: int = Field(default=60)
    
    # Database
    MONGO_URI: str = Field(default_factory=lambda: os.getenv("MONGO_URI", "mongodb://localhost:27017"))
    DATABASE_NAME: str = Field(default_factory=lambda: os.getenv("DATABASE_NAME", "proofnexa"))
    COLLECTION_NAME: str = Field(default_factory=lambda: os.getenv("COLLECTION_NAME", "submissions"))

    class Config:
        env_file = ".env"

settings = Settings()
