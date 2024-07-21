from __future__ import annotations

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped
from fastapi.security import OAuth2PasswordBearer

from app.database.main import Base

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    todos: Mapped[list["Todo"]] = relationship("Todo", back_populates="owner")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
