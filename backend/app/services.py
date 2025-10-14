from app.clients.chatApiClient import openAIClient
from openai.types.chat import ChatCompletionMessageParam
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.responses import StreamingResponse
import json

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

        await collection.update_one(
            {"uuid": chat_id},
            {"$set": {"history": history}},
            upsert=True
        )

        
        async def event_stream():
            assistant_message = ""
            counter = 1
            async for chunk in openAIClient.send_message(messages=history):
                counter += 1
                assistant_message += chunk
                yield f"id:{counter}\nevent:chatCompletion\ndata:{json.dumps(chunk)}\n\n"
            history.append({"role": "assistant", "content": assistant_message})
            await collection.update_one(
                {"uuid": chat_id},
                {"$set": {"history": history}},
                upsert=True
            )

        return StreamingResponse(event_stream(), media_type="text/event-stream")
