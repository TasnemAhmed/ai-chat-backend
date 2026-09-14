from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models import User, Conversation
from app.schemas.conversation import ConversationCreate, ConversationResponse

router = APIRouter()

@router.post("/users/{user_id}/conversations")
def create_conversation(user_id:int,converstion_data:ConversationCreate):
    db = SessionLocal()
    user=db.get(User,user_id)
    if user is None:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    conversation=Conversation(
        user_id=user_id,
        title=converstion_data.title
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    db.close()

#GET CONVERSATION
@router.get("/users/{user_id}/conversations")
def get_user_conversations(user_id:int):
    db=SessionLocal()
    user = db.get(User,user_id)
    if user is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    conversations = user.conversations

    db.close()

    return [
        {
            "id": conversation.id,
            "user_id": conversation.user_id,
            "title": conversation.title
        }
        for conversation in conversations
    ]

