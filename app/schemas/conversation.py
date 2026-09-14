from pydantic import BaseModel , ConfigDict


class ConversationCreate(BaseModel):
    title: str

class ConversationResponse(BaseModel):
    id: int
    user_id: int
    title: str