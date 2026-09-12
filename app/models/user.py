from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    conversations: Mapped[list["Conversation"]] = relationship(
    back_populates="user"
)