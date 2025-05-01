from fastapi import APIRouter, HTTPException, Depends, Form
from pydantic import BaseModel
from typing import List, Optional
from app.models.chatbot import AirlineChatbot

# Initialize router
router = APIRouter()

# Initialize chatbot
chatbot = AirlineChatbot()

# Define request and response models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    conversation_history: List[ChatMessage]

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return a response
    """
    try:
        # Process the user message
        response = chatbot.process_message(request.message)
        
        # Return the response and updated conversation history
        return ChatResponse(
            response=response,
            conversation_history=chatbot.memory.get_conversation_history()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@router.post("/clear")
async def clear_conversation():
    """
    Clear the current conversation history
    """
    message = chatbot.clear_conversation()
    return {"message": message}