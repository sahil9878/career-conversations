import dotenv
import os
from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional


dotenv.load_dotenv()

class MongoClient:

    async def connect(self):
        uri = os.getenv("MONGO_DB_CONNECTION_STRING", "")
        db_name = os.getenv("MONGO_DATABASE_NAME", "")
        self.client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
        print("Connected to MongoDB...")

        self.db = self.client[db_name]

    async def disconnect(self):
        if self.client:
            print("Disconnecting from MongoDB...")
            self.client.close() 

    async def get_context(self) -> str:
        collection = self.db["context"]
        document = await collection.find_one({"name": "context"})
        if document:
            return document.get("text", "")
        return ""
    
    async def log_leads(self, email: str, name:str, notes: str, phone: Optional[str] = None) -> None:
        collection = self.db["leads"]
        document = {
            "email": email,
            "name": name,
            "notes": notes,
            "phone": phone
        }
        await collection.insert_one(document)

    async def log_unknown_question(self, question:str="") -> None:
        collection = self.db["unknown_questions"]
        document = {
            "question": question,
        }
        await collection.insert_one(document)


mongo = MongoClient()