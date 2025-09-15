from fastapi import FastAPI
from pydantic import BaseModel
from app.routes import router 
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.clients.mongoClient import mongo
from app.clients.chatApiClient import openAIClient
from contextlib import asynccontextmanager
import os
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await mongo.connect()
    await openAIClient.warmup()
    yield
    await mongo.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(router)

origins_string = os.getenv("FRONTEND_URL", "http://localhost:5173")
origins = origins_string.split(",")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


