from app.clients.mongoClient import mongo
from motor.motor_asyncio import AsyncIOMotorDatabase


def get_db() -> AsyncIOMotorDatabase | None:
    return mongo.db

