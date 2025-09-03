from fastapi import APIRouter

router = APIRouter(prefix="/chat")
from app.controllers import ChatController
from app.modes import ChatRequest

@router.post("/")
async def sendMessage(request: ChatRequest):
    return await ChatController.sendMessage(request.message)