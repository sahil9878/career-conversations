from fastapi import APIRouter, Depends
from app.dependencies import get_db

router = APIRouter(prefix="/chat")
from app.controllers import ChatController
from app.modes import ChatRequest

@router.post("/")
async def sendMessage(request: ChatRequest, db = Depends(get_db)):
    return await ChatController.sendMessage(db, message=request.message, chat_id=request.chat_id)