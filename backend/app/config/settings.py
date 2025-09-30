import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # CORS Settings
    allowed_origins: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    # LLM Settings
    model_name: str = "gpt3-turbo"  # Base model
    fine_tuned_model_path: Optional[str] = "./models/fine_tuned"
    use_fine_tuned: bool = False
    max_length: int = 512
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    
    # Story Settings
    min_story_length: int = 100
    max_story_length: int = 2000
    max_characters: int = 5
    max_character_name_length: int = 30
    
    # Session Settings
    session_timeout_hours: int = 24
    
    # Dataset Settings
    dataset_path: str = "./data/story_dataset.csv"
    fine_tune_train_path: str = "./data/fine_tune_data/train_stories.jsonl"
    fine_tune_val_path: str = "./data/fine_tune_data/val_stories.jsonl"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def get_model_path(self) -> str:
        if self.use_fine_tuned and self.fine_tuned_model_path:
            if os.path.exists(self.fine_tuned_model_path):
                return self.fine_tuned_model_path
        return self.model_name

# Global settings instance
settings = Settings()