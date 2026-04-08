from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.models.chat_schema import ChatRequest, ChatResponse
from typing import Optional
from src.chatbot.chat import create_fashion_chatbot

router = APIRouter(prefix="/fashion", tags=["fashion"])

bot = create_fashion_chatbot()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Send a message and get a fashion recommendation."""
    try:
        result = bot.chat(
            user_message=request.message,
            user_id=request.user_id,
            session_id=request.session_id,
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}")
def get_history(session_id: str):
    """Return the raw chat history for a given session."""
    session = bot._sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    history = [
        {"role": msg.role, "text": msg.parts[0].text}
        for msg in session.get_history()
    ]
    return {"session_id": session_id, "history": history}


@router.get("/profile/{user_id}")
def get_profile(user_id: str, session_id: Optional[str] = None):
    """Return the current memory profile for a user."""
    profile = bot.memory.get_user_profile(user_id, session_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found.")
    return {"user_id": user_id, "profile": profile}