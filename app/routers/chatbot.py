from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chatbot import ChatbotService

router = APIRouter(
    prefix="/chatbot",
    tags=["Chatbot"],
)


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = ChatbotService().ask(request.message)
    return ChatResponse(reply=reply)


@router.get("/health")
def health():
    service = ChatbotService()
    configured = bool(service.api_key and service.api_key != "your_openai_api_key_here")
    return {"configured": configured}