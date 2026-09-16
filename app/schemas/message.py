from pydantic import BaseModel, ConfigDict, Field
from enum import Enum


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"


class MessageCreate(BaseModel):
    role: MessageRole
    content: str = Field(min_length=1)


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    image_url: str | None = None
    image_mime_type: str | None = None

    model_config = ConfigDict(from_attributes=True)
