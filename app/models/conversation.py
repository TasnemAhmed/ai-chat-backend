from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str]
    user: Mapped["User"] = relationship(
    back_populates="conversations"
)
    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation"
    )