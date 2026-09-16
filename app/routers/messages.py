from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
import os
from google import genai
from app.database import SessionLocal
from app.models import Conversation, Message
from app.schemas.message import MessageCreate, MessageResponse
from dotenv import load_dotenv
from google.genai import types
from app.ai.config import MODEL_NAME, SYSTEM_PROMPT, TEMPERATURE
from app.dependencies import get_current_user

load_dotenv()

router = APIRouter()

client = genai.Client(
    api_key=os.getenv("YOUR_API_KEY")
)


@router.post("/conversations/{conversation_id}/messages")
def add_message(
    conversation_id: int,
    message: MessageCreate,
    current_user=Depends(get_current_user)
):
    db = SessionLocal()

    conv = db.get(Conversation, conversation_id)

    if conv is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    # Authorization: make sure the conversation belongs to the current user
    if conv.user_id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail="You cannot access another user's conversation"
        )

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
def chat(
    conversation_id: int,
    message: MessageCreate,
    current_user=Depends(get_current_user)
):
    db = SessionLocal()

    conversation = db.get(Conversation, conversation_id)

    if conversation is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    # Authorization: make sure the conversation belongs to the current user
    if conversation.user_id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail="You cannot access another user's conversation"
        )

    user_message = Message(
        conversation_id=conversation_id,
        role="user",
        content=message.content
    )

    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    messages = db.scalars(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.id)
    ).all()

    history = []

    for msg in messages:
        role = "model" if msg.role == "assistant" else "user"

        history.append({
            "role": role,
            "parts": [
                {"text": msg.content}
            ]
        })

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=history,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=TEMPERATURE
        )
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


@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[MessageResponse]
)
def get_messages(
    conversation_id: int,
    current_user=Depends(get_current_user)
):
    db = SessionLocal()

    conversation = db.get(Conversation, conversation_id)

    if conversation is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    # Authorization: make sure the conversation belongs to the current user
    if conversation.user_id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail="You cannot access another user's conversation"
        )

    messages = db.scalars(
        select(Message)
        .where(Message.conversation_id == conversation_id)
    ).all()

    db.close()

    return messages

