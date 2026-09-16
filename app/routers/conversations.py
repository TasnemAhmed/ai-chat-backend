from fastapi import APIRouter, HTTPException, Depends
from app.database import SessionLocal
from app.models import User, Conversation
from app.schemas.conversation import ConversationCreate, ConversationResponse
from app.dependencies import get_current_user
router = APIRouter()

@router.post("/users/{user_id}/conversations")
def create_conversation(
    user_id: int,
    conversation_data: ConversationCreate,
    current_user: User = Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot create a conversation for another user"
        )

    db = SessionLocal()

    user = db.get(User, user_id)

    if user is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    conversation = Conversation(
        user_id=current_user.id,
        title=conversation_data.title
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    db.close()

    return conversation
#GET CONVERSATION
@router.get("/users/{user_id}/conversations")
def get_user_conversations(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot access another user's conversations"
        )

    db = SessionLocal()

    user = db.get(User, user_id)

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