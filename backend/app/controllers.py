
from app.services import ChatService
from motor.motor_asyncio import AsyncIOMotorDatabase
class ChatController:
    
    @staticmethod
    async def sendMessage(db:AsyncIOMotorDatabase, message: str , chat_id: str = ""):
        return await ChatService.sendMessage(db, message=message, chat_id=chat_id)