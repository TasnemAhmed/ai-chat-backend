from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from app.models import User, Conversation ,Message
from app.schemas.conversation import ConversationCreate
from app.database import SessionLocal, Base, engine
from app.schemas.message import MessageCreate,MessageResponse
from app.routers import messages , conversations , users

from app.schemas.user import UserCreate

import app.models

app = FastAPI()

Base.metadata.create_all(engine)
app.include_router(messages.router)
app.include_router(conversations.router)
app.include_router(users.router)

    #uvicorn app.main:app --reload