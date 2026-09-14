from fastapi import APIRouter, HTTPException
from sqlalchemy import select
import os
from google import genai
from app.database import SessionLocal
from app.models import Conversation, Message
from app.schemas.message import MessageCreate, MessageResponse

router = APIRouter()

client = genai.Client(
    api_key=os.getenv("YOUR_API_KEY")
)
@router.post("/conversations/{conversation_id}/messages")
def add_message(conversation_id: int,message:MessageCreate):
    db=SessionLocal()
    conv=db.get(Conversation,conversation_id)
    if conv is None:
        db.close()
        raise HTTPException(status_code=404, detail="Conversation not found")

    new_message = Message(
        conversation_id=conversation_id,
        role=message.role,
        content=message.content
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    db.close()

    return new_message


@router.post("/conversations/{conversation_id}/chat")
def chat(conversation_id: int, message: MessageCreate):

    db = SessionLocal()

    conversation = db.get(Conversation, conversation_id)

    if conversation is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    user_message = Message(
        conversation_id=conversation_id,
        role="user",
        content=message.content
    )

    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=message.content
    )
    assistant_message = Message(
    conversation_id=conversation_id,
    role="assistant",
    content=response.text
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)
    


    db.close()

    return {
        "user_message": message.content,
        "ai_response": response.text
    }
@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageResponse])
def get_messages(conversation_id: int):

    db = SessionLocal()

    conversation = db.get(Conversation, conversation_id)

    if conversation is None:
        db.close()
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = db.scalars(
        select(Message).where(Message.conversation_id == conversation_id)
    ).all()

    db.close()

    return messages