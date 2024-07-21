from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING
from app.database.main import Base

if TYPE_CHECKING:
    from app.models.user import User


class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
    ended = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    edited_at = Column(DateTime, default=datetime.now())
    completed_at = Column(DateTime, default=None)
    ending_at = Column(DateTime, default=None)
    deleted_at = Column(DateTime, default=None)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner: Mapped[User] = relationship("User", back_populates="todos")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
