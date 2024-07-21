from datetime import datetime

from pydantic import BaseModel


class CreateTodoPayload(BaseModel):
    title: str
    description: str
    owner_id: int


class UpdateTodoPayload(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None
    ended: bool = None
    deleted: bool = None
    edited_at: datetime = datetime.now()
    completed_at: datetime = None
    ending_at: datetime = None
    deleted_at: datetime = None


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    ended: bool
    deleted: bool
    edited_at: datetime
    completed_at: datetime
    ending_at: datetime
    deleted_at: datetime
    owner_id: int

    class Config:
        from_attributes = True
