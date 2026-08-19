import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database - SQLite for MVP
    DATABASE_URL: str = "sqlite:///./interviewos.db"
    
    # API
    API_TITLE: str = "InterviewOS API"
    API_VERSION: str = "0.1.0"
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # Gemini API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

settings = Settings()