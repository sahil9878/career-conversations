from app.clients import OpenAIClient

class ChatService:
    @staticmethod
    async def sendMessage(message: str):
        response = await OpenAIClient.send_message(message)
        return {"response": response}