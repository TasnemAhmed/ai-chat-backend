from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from app.models import User, Conversation ,Message
from app.schemas.conversation import ConversationCreate
from app.database import SessionLocal, Base, engine
from app.schemas.message import MessageCreate,MessageResponse


from app.schemas.user import UserCreate

import app.models

app = FastAPI()

Base.metadata.create_all(engine)



# =========================
# Create User
# =========================

@app.post("/users")
def create_user(user_data: UserCreate):

    db = SessionLocal()

    user = User(
        name=user_data.name,
        email=user_data.email
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    db.close()

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }

# =========================
# get Users
# =========================

@app.get("/users")
def get_users():

    db = SessionLocal()

    users = db.scalars(select(User)).all()

    db.close()

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        for user in users
    ]


# =========================
# get User by Id
# =========================

@app.get("/users/{id}")
def get_users(id:int):

    db = SessionLocal()

    user = db.get(User,id)
    user = db.get(User, id)

    if user is None :
        db.close()
        raise HTTPException(
        status_code=404,
        detail="User not found"
    )
    db.close()

    return{
            "id": user.id,
            "name": user.name,
            "email": user.email
        }

# =========================
# update User by Id
# =========================


@app.put("/users/{id}")
def update_user(id:int,user_data:UserCreate):
    dp=SessionLocal()

    user=dp.get(User,id)

    if user is None :
            dp.close()
            raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    user.name=user_data.name
    user.email=user_data.email

    dp.commit()
    dp.refresh(user)
    dp.close()

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email 
    }

# =========================
# delete User by Id
# =========================

@app.delete("/users/{id}")
def delete_user(id: int):

    db = SessionLocal()

    user = db.get(User, id)

    if user is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    db.close()

    return {
        "message": "User deleted successfully"
    }
#-------CONVERSATION---------
@app.post("/users/{user_id}/conversations")
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
@app.get("/users/{user_id}/conversations")
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


@app.post("/conversations/{conversation_id}/messages")
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

@app.get("/conversations/{conversation_id}/messages", response_model=list[MessageResponse])
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
    #uvicorn app.main:app --reload