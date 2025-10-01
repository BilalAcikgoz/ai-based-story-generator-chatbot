from typing import Dict, Optional, Tuple
from models.schemas import ChatMessage, StoryParams, MessageRole
from utils.validators import (
    validate_age_group, validate_genre, 
    validate_length, validate_prompt, validate_characters,
    sanitize_input
)
from core.prompts import StoryPrompts
import uuid
from datetime import datetime, timedelta

class Session:
    # Session storage
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.messages: list = []
        self.params: Dict = {}
        self.state = "greeting"
        self.created_at = datetime.now()
        self.story: Optional[str] = None

class ChatService:
    # Manages chat sessions and conversation flow
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self.prompts = StoryPrompts.get_collection_prompts()
        self._cleanup_interval = timedelta(hours=24)
    
    def create_session(self) -> Session:
        # Create new session
        session = Session()
        self.sessions[session.id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        # Get existing session
        session = self.sessions.get(session_id)
        
        if session and (datetime.now() - session.created_at) > self._cleanup_interval:
            del self.sessions[session_id]
            return None
        
        return session
    
    def cleanup_old_sessions(self) -> int:
        # Remove expired sessions
        expired = [
            sid for sid, sess in self.sessions.items()
            if (datetime.now() - sess.created_at) > self._cleanup_interval
        ]
        for sid in expired:
            del self.sessions[sid]
        return len(expired)
    
    def process_message(self, session_id: Optional[str], user_message: str) -> Tuple[str, str, Optional[StoryParams], bool]:
        # Sanitize input
        user_message = sanitize_input(user_message)
        
        # Get or create session
        if session_id:
            session = self.get_session(session_id)
            if not session:
                session = self.create_session()
        else:
            session = self.create_session()
        
        # Add user message
        session.messages.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now()
        })
        
        # Process based on state
        if session.state == "greeting":
            response = self.prompts["greeting"]
            session.state = "age"
        
        elif session.state == "age":
            response, session.state = self._handle_age(session, user_message)
        
        elif session.state == "genre":
            response, session.state = self._handle_genre(session, user_message)
        
        elif session.state == "length":
            response, session.state = self._handle_length(session, user_message)
        
        elif session.state == "topic":
            response, session.state = self._handle_topic(session, user_message)
        
        elif session.state == "characters":
            response, session.state = self._handle_characters(session, user_message)
        
        elif session.state == "done":
            response = "Write 'new story' for a new story!"
            if "new" in user_message.lower():
                session.params = {}
                session.state = "greeting"
                response = self.prompts["greeting"]
        
        else:
            response = "Something went wrong. Let's start over!"
            session.state = "greeting"
        
        # Add bot message
        session.messages.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now()
        })
        
        # Check if ready for generation
        is_complete = session.state == "generating"
        story_params = None
        
        if is_complete:
            story_params = StoryParams(**session.params)
        
        return response, session.id, story_params, is_complete
    
    def _handle_age(self, session: Session, message: str) -> Tuple[str, str]:
        msg_lower = message.lower().strip()
        
        age_mapping = {
            "3-5": ["3-5", "3", "4", "5", "üç", "dört", "beş", "küçük"],
            "6-10": ["6-10", "6", "7", "8", "9", "10", "altı", "yedi", "sekiz", "orta"],
            "11-15": ["11-15", "11", "12", "13", "14", "15", "onbir", "oniki", "büyük"]
        }
        
        for age_group, keywords in age_mapping.items():
            if any(k in msg_lower for k in keywords):
                if validate_age_group(age_group):
                    session.params["age_group"] = age_group
                    return self.prompts["genre"], "genre"
        
        return "Please select a valid age group: 3-5, 6-10, or 11-15", "age"
    
    def _handle_genre(self, session: Session, message: str) -> Tuple[str, str]:
        msg_lower = message.lower().strip()
        
        genre_mapping = {
            "adventure": ["macera", "adventure", "serüven"],
            "fantasy": ["fantastik", "fantasy", "sihir", "büyü"],
            "friendship": ["arkadaşlık", "friendship", "arkadaş"],
            "educational": ["eğitici", "educational", "öğretici"],
            "animal": ["hayvan", "animal"],
            "family": ["aile", "family"],
            "nature": ["doğa", "nature"],
            "science": ["bilim", "science"],
            "mystery": ["gizem", "mystery", "sır"],
            "humor": ["komedi", "humor", "komik", "eğlenceli"]
        }
        
        for genre, keywords in genre_mapping.items():
            if any(k in msg_lower for k in keywords):
                if validate_genre(genre):
                    session.params["genre"] = genre
                    return self.prompts["length"], "length"
        
        return "Lütfen geçerli bir tür seç (macera, fantastik, arkadaşlık, vb.)", "genre"
    
    def _handle_length(self, session: Session, message: str) -> Tuple[str, str]:
        msg_lower = message.lower().strip()
        
        length_mapping = {
            "short": ["kısa", "short", "kisa"],
            "medium": ["orta", "medium"],
            "long": ["uzun", "long"]
        }
        
        for length, keywords in length_mapping.items():
            if any(k in msg_lower for k in keywords):
                if validate_length(length):
                    session.params["length"] = length
                    return self.prompts["topic"], "topic"
        
        return "Please select a valid length: short, medium, or long", "length"
    
    def _handle_topic(self, session: Session, message: str) -> Tuple[str, str]:
        is_valid, error = validate_prompt(message)
        
        if is_valid:
            session.params["topic"] = message.strip()
            return self.prompts["characters"], "characters"
        
        return f"The topic is not suitable: {error}. Please write a child-friendly topic.", "topic"
    
    def _handle_characters(self, session: Session, message: str) -> Tuple[str, str]:
        msg_lower = message.lower().strip()
        
        if any(word in msg_lower for word in ["hayır", "yok", "no", "istemiyorum"]):
            session.params["characters"] = None
            return self.prompts["generating"], "generating"
        
        characters = [c.strip() for c in message.split(',') if c.strip()]
        
        if characters:
            is_valid, error = validate_characters(characters)
            if is_valid:
                session.params["characters"] = characters
                return self.prompts["generating"], "generating"
            return f"Character names are not appropriate: {error}", "characters"
        
        return "Write character names separated by commas or say 'no'.", "characters"
    
    def set_story(self, session_id: str, story: str):
        # Set generated story
        session = self.get_session(session_id)
        if session:
            session.story = story
            session.state = "done"

# Global instance
chat_service = ChatService()