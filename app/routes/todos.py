from fastapi import APIRouter, HTTPException

from app.controllers.todo import *
from app.schemas.todo import CreateTodoPayload, UpdateTodoPayload

router = APIRouter()


@router.get("/todos")
async def get(skip: int = 0, limit: int = 100):
    todos = await get_todos(skip, limit)
    return todos


@router.get("/todos/{todo_id}")
async def get_by_id(todo_id: int):
    todo = await get_todo_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.post("/todos")
async def create(todo: CreateTodoPayload):
    return await create_todo(todo)


@router.put("/todos/{todo_id}")
async def update(todo_id: int, todo: UpdateTodoPayload):
    return await update_by_id(todo_id, todo)


@router.delete("/todos/{todo_id}")
async def delete(todo_id: int):
    return await delete_by_id(todo_id)
