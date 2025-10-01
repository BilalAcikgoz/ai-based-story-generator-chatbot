from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, ChatResponse, HealthResponse
from services.chat_service import chat_service
from services.llm_service import llm_service
from core.prompts import StoryPrompts

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Chat endpoint for story generation conversation
    try:
        # Process user message
        response, session_id, story_params, is_complete = chat_service.process_message(
            request.session_id,
            request.message
        )
        
        # If ready to generate story
        story = None
        if is_complete and story_params:
            # Build prompt
            prompt = StoryPrompts.build_story_prompt(story_params.dict())
            
            # Generate story
            story = await llm_service.generate_story(prompt)
            
            # Save story to session
            chat_service.set_story(session_id, story)
        
        return ChatResponse(
            session_id=session_id,
            message=response,
            story_params=story_params,
            story=story,
            is_complete=is_complete
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="healthy",
        model_loaded=llm_service.is_loaded(),
        model_name=llm_service.get_model_name()
    )

@router.post("/cleanup")
async def cleanup_sessions():
    count = chat_service.cleanup_old_sessions()
    return {"cleaned_sessions": count}