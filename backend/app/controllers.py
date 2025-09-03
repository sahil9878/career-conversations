
from app.services import ChatService

class ChatController:
    
    @staticmethod
    async def sendMessage(message: str):
        return await ChatService.sendMessage(message)