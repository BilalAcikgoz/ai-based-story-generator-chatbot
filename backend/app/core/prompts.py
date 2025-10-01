from typing import Dict

class StoryPrompts:
    # Story generation prompt templates
    
    # Age-specific instructions
    AGE_PROMPTS = {
        "3-5": """Write a story for very young children (ages 3-5).
               RULES:
               - Use very simple and short sentences
               - Include repetitive words and rhythm
               - Use colorful and fun words
               - Each sentence should be understandable
               - Use a positive and happy tone""",
        
        "6-10": """Write a story for school-aged children (ages 6-10).
                RULES:
                - Use clear but rich vocabulary
                - Teach simple moral lessons
                - Stimulate the imagination
                - Add adventure and excitement
                - Be fun and engaging""",
        
        "11-15": """Write a story for older children (ages 11-15).
                 RULES:
                 - Use rich vocabulary
                 - Develop deeper characters
                 - Develop an interesting plot
                 - Teach values ​​and lessons
                 - Be engaging"""
    }
    
    # Genre-specific additions
    GENRE_PROMPTS = {
            "adventure": "Write an adventure story filled with excitement, discovery, and courage.",
            "fantasy": "Write a story featuring magic, enchantment, and fantastical creatures.",
            "friendship": "Write a story about friendship, cooperation, and love.",
            "educational": "Write an educational and instructive yet very entertaining story.",
            "animal": "Write a story filled with cute animal characters.",
            "family": "Write a heartwarming story about family values ​​and love.",
            "nature": "Write a story about nature, the environment, and animals.",
            "science": "Write an interesting story about science and exploration.",
            "mystery": "Write an exciting story about mystery and puzzle solving.",
            "humor": "Write a funny and entertaining story that will make you laugh."
    }
    
    # Length specifications
    LENGTH_SPECS = {
        "short": "Write a short story (approximately 200-300 words).",
        "medium": "Write a medium-length story (approximately 400-600 words).",
        "long": "Write a long and detailed story (approximately 800-1000 words)."
    }
    
    @staticmethod
    def build_story_prompt(params: Dict) -> str:
        # Build complete story generation prompt
        
        age_group = params.get("age_group", "6-10")
        genre = params.get("genre", "adventure")
        length = params.get("length", "medium")
        topic = params.get("topic", "")
        characters = params.get("characters", [])
        
        # Get instructions
        age_instruction = StoryPrompts.AGE_PROMPTS.get(age_group)
        genre_instruction = StoryPrompts.GENRE_PROMPTS.get(genre)
        length_instruction = StoryPrompts.LENGTH_SPECS.get(length)
        
        # Build character section
        character_section = ""
        if characters:
            char_names = ", ".join(characters)
            character_section = f"\nCHARACTERS: {char_names} use named characters."
        
        # Build complete prompt
        prompt = f"""You are a professional children's story writer.

                {age_instruction}

                GENRE: {genre_instruction}

                LENGTH: {length_instruction}

                TOPIC: {topic}{character_section}

                IMPORTANT:
                1. Start the story with a catchy title
                2. Write fluently and engagingly
                3. Use child-friendly language
                4. Be safe and educational
                5. End with a happy or educational ending

                Now write the story:"""
        
        return prompt
    
    @staticmethod
    def get_collection_prompts() -> Dict[str, str]:
        return {
            "greeting": """Hello! I'm your story assistant!

            I can write a special story for you. First, I'll ask you a few questions.

            How old are you?
            - 3-5 years
            - 6-10 years
            - 11-15 years
            """,

            "genre": """Great! What kind of story would you like?

            - Adventure
            - Fantasy
            - Friendship
            - Educational
            - Animal stories
            - Family
            - Nature
            - Science
            - Mystery
            - Comedy
            """,

            "length": """Perfect! How long should the story be?

            - Short - 2-3 minutes
            - Medium - 5-7 minutes
            - Long - 10+ minutes
            """,

            "topic": """Great! Now for the most important part:

            What should the story be about? Tell me about it!""",

            "characters": """Great plot!

            Should the story include special character names?
            If so, write their names (separated by commas), otherwise, say 'no'.""",

            "generating": """I've got all the information!

            Now I'm writing a special story for you..."""
        }