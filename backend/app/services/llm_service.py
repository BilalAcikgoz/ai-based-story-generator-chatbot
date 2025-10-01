from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from typing import Optional
import os
from config.settings import settings
from utils.validators import validate_story_output

class LLMService:
    # LLM service for story generation
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._loaded = False
        self._model_name = settings.model_name
        
    def load_model(self):
        # Load the language model
        if self._loaded:
            print("Model already loaded")
            return
        
        try:
            model_path = settings.get_model_path()
            print(f"Loading model from: {model_path}")
            print(f"Device: {self.device}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            
            # Set pad token if not exists
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                low_cpu_mem_usage=True
            )
            
            # Move to device
            self.model.to(self.device)
            self.model.eval()
            
            # Create pipeline
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1
            )
            
            self._loaded = True
            self._model_name = model_path
            print("Model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def is_loaded(self) -> bool:
        return self._loaded
    
    def get_model_name(self) -> str:
        return self._model_name
    
    async def generate_story(self, prompt: str) -> str:
        if not self._loaded:
            self.load_model()
        
        try:
            # Generate text
            outputs = self.pipeline(
                prompt,
                max_length=settings.max_length,
                temperature=settings.temperature,
                top_p=settings.top_p,
                top_k=settings.top_k,
                do_sample=True,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.2,
                no_repeat_ngram_size=3
            )
            
            # Extract generated text
            generated_text = outputs[0]['generated_text']
            
            # Remove the prompt from output
            story = generated_text[len(prompt):].strip()
            
            # Post-process the story
            story = self._post_process_story(story)
            
            # Validate output
            is_valid, error = validate_story_output(
                story, 
                settings.min_story_length, 
                settings.max_story_length
            )
            
            if not is_valid:
                print(f"Generated story validation failed: {error}")
                # Return a fallback story
                story = self._get_fallback_story()
            
            return story
            
        except Exception as e:
            print(f"Error generating story: {e}")
            return self._get_fallback_story()
    
    def _post_process_story(self, text: str) -> str:
        if not text:
            return ""
        
        # Remove incomplete sentences at the end
        if text and not text[-1] in ['.', '!', '?']:
            # Find last complete sentence
            last_punct = max(
                text.rfind('.'),
                text.rfind('!'),
                text.rfind('?')
            )
            if last_punct > 0:
                text = text[:last_punct + 1]
        
        # Clean up extra whitespace
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        text = '\n\n'.join(lines)
        
        # Ensure proper spacing after punctuation
        import re
        text = re.sub(r'([.!?])([A-Z])', r'\1 \2', text)
        
        return text.strip()
    
    def _get_fallback_story(self) -> str:
        # Return a fallback story if generation fails
        return """# Little Hero

Once upon a time, there lived a brave boy in a small town. Every day, he sought new adventures and played fun games with his friends.
One day, he found a little cat lost in the town park. The cat was very sad and scared. The boy decided to help the cat.
He searched all day for the cat's owner. He knocked on every door, asking everyone. Finally, he found a family who missed the cat very much.
The family was overjoyed and thanked the boy. The boy learned how beautiful it was to help.
From that day on, he always tried to help others. And so, he became the little hero."""
    
    def unload_model(self):
        # Unload model from memory
        if self._loaded:
            del self.model
            del self.tokenizer
            del self.pipeline
            torch.cuda.empty_cache()
            self._loaded = False
            print("Model unloaded")

# Global instance
llm_service = LLMService()

# Load model on import (optional - can be lazy loaded)
# llm_service.load_model()