from typing import List, Tuple
import re

# Available options
VALID_AGE_GROUPS = ["3-5", "6-10", "11-15"]
VALID_GENRES = [
    "adventure", "fantasy", "friendship", "educational", 
    "animal", "family", "nature", "science", "mystery", "humor"
]
VALID_LENGTHS = ["short", "medium", "long"]

# Inappropriate words for content filtering
INAPPROPRIATE_WORDS = [
    'violence', 'blood', 'death', 'kill', 'murder', 'weapon', 'gun', 'knife',
    'hate', 'scary', 'horror', 'nightmare', 'devil', 'hell',
    'drug', 'alcohol', 'smoke', 'cigarette', 'sex', 'war'
]

def validate_age_group(age_group: str) -> bool:
    return age_group in VALID_AGE_GROUPS

def validate_genre(genre: str) -> bool:
    return genre in VALID_GENRES

def validate_length(length: str) -> bool:
    return length in VALID_LENGTHS

def validate_prompt(prompt: str) -> Tuple[bool, str]:
    if not prompt or not prompt.strip():
        return False, "Subject cannot be empty"
    
    cleaned = prompt.strip()
    
    if len(cleaned) < 10:
        return False, "Subject must be at least 10 characters"
    
    if len(cleaned) > 500:
        return False, "Subject can be up to 500 characters"
    
    # Check for inappropriate content
    prompt_lower = cleaned.lower()
    for word in INAPPROPRIATE_WORDS:
        if word in prompt_lower:
            return False, "Inappropriate content detected. Choose a child-friendly topic"
    
    # Check for excessive special characters
    special_chars = len(re.findall(r'[^a-zA-Z0-9\s\.,!?;:\-çğıöşüÇĞIİÖŞÜ]', cleaned))
    if special_chars > len(cleaned) * 0.1:
        return False, "There are too many special characters"
    
    return True, ""

def validate_characters(characters: List[str]) -> Tuple[bool, str]:
    if not characters:
        return True, ""
    
    if len(characters) > 5:
        return False, "A maximum of 5 characters can be added"
    
    for char in characters:
        if not char or not char.strip():
            return False, "Character name cannot be empty"
        
        cleaned = char.strip()
        
        if len(cleaned) > 30:
            return False, f"'{cleaned}' the name is too long (max 30 characters)"
        
        if len(cleaned) < 2:
            return False, f"'{cleaned}' the name is too short (min 2 characters)"
        
        # Only letters, spaces, hyphens allowed
        if not re.match(r"^[a-zA-ZğüşıöçĞÜŞİÖÇ\s\-']+$", cleaned):
            return False, f"'{cleaned}' contains invalid characters"
        
        # Check inappropriate names
        char_lower = cleaned.lower()
        for word in INAPPROPRIATE_WORDS:
            if word in char_lower:
                return False, f"'{cleaned}' contains inappropriate content"
    
    # Check duplicates
    cleaned_names = [c.strip().lower() for c in characters]
    if len(cleaned_names) != len(set(cleaned_names)):
        return False, "There can be no repeating character names"
    
    return True, ""

def sanitize_input(text: str) -> str:
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove dangerous characters but keep Turkish chars
    text = re.sub(r'[^\w\s\.,!?;:\-\'\"çğıöşüÇĞIİÖŞÜ]', '', text)
    
    # Limit consecutive punctuation
    text = re.sub(r'([.!?]){3,}', r'\1\1\1', text)
    
    return text.strip()

def is_safe_content(text: str) -> bool:
    if not text:
        return True
    
    text_lower = text.lower()
    
    for word in INAPPROPRIATE_WORDS:
        if word in text_lower:
            return False
    
    return True

def validate_story_output(story: str, min_length: int = 100, max_length: int = 2000) -> Tuple[bool, str]:
    if not story or not story.strip():
        return False, "Story is empty"
    
    cleaned = story.strip()
    
    if len(cleaned) < min_length:
        return False, f"The story is too short (min {min_length} character)"
    
    if len(cleaned) > max_length:
        return False, f"The story is too long (max {max_length} character)"
    
    if not is_safe_content(cleaned):
        return False, "The story contains inappropriate content"
    
    # Check minimum sentences
    sentences = re.split(r'[.!?]+', cleaned)
    valid_sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
    
    if len(valid_sentences) < 3:
        return False, "The story must contain at least 3 sentences"
    
    return True, ""