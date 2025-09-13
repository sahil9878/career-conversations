from app.clients.chatApiClient import openAIClient
from openai.types.chat import ChatCompletionMessageParam
from motor.motor_asyncio import AsyncIOMotorDatabase
class ChatService:
    @staticmethod
    async def sendMessage(db:AsyncIOMotorDatabase, message: str, chat_id: str = "" ):
        collection = db["chat_logs"]
        chat = await collection.find_one({"uuid": chat_id})
        history: list[ChatCompletionMessageParam] = []
        if chat:
            history = chat["history"] if "history" in chat else []
        else:
            new_chat = {"uuid": chat_id, "history": []}
            chat = await collection.insert_one(new_chat)
        history.append({"role": "user", "content": message})

        response = await openAIClient.send_message(messages=history)

        history.append({"role": "assistant", "content": response})
        
        await collection.update_one(
            {"uuid": chat_id},
            {"$set": {"history": history}},
            upsert=True
        )
        return {"response": response}