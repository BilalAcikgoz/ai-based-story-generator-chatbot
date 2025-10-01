from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    # Message roles
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessage(BaseModel):
    # Single chat message
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        use_enum_values = True

class StoryParams(BaseModel):
    # Story generation parameters
    age_group: str
    genre: str
    length: str
    topic: str
    characters: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "age_group": "6-10",
                "genre": "adventure",
                "length": "medium",
                "topic": "An astronaut's adventure in space",
                "characters": ["Tom", "Hermione"]
            }
        }

class ChatRequest(BaseModel):
    # Chat API request
    session_id: Optional[str] = None
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": None,
                "message": "6-10 age"
            }
        }

class ChatResponse(BaseModel):
    # Chat API response
    session_id: str
    message: str
    story_params: Optional[StoryParams] = None
    story: Optional[str] = None
    is_complete: bool = False
    
    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "session_id": "123e4567-e89b-12d3-a456-426614174000",
                "message": "Great! I will prepare a story for the 6-10 age group.",
                "story_params": None,
                "story": None,
                "is_complete": False
            }
        }

class HealthResponse(BaseModel):
    # Health check response
    status: str
    model_loaded: bool
    model_name: str