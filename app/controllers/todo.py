from app.database.main import get_db
from app.models.todo import Todo
from app.schemas.todo import CreateTodoPayload, UpdateTodoPayload, TodoResponse
from fastapi import HTTPException

from sqlalchemy.future import select


async def get_todos(skip: int = 0, limit: int = 100):
    try:
        async with get_db() as db:
            result = await db.execute(select(Todo).offset(skip).limit(limit))
            todos = result.scalars().all()
            return [TodoResponse.model_validate(todo) for todo in todos]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")


async def get_todo_by_id(todo_id: int):
    try:
        async with get_db() as db:
            result = await db.execute(select(Todo).filter(Todo.id == todo_id))
            todo = result.scalars().first()
            if not todo:
                raise HTTPException(status_code=404, detail="Todo not found")
            return TodoResponse.model_validate(todo)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")


async def create_todo(todo: CreateTodoPayload):
    try:
        async with get_db() as db:
            db_todo = Todo(
                title=todo.title,
                description=todo.description,
                owner_id=todo.owner_id,
            )
            await db.add(db_todo)
            await db.commit()
            return db_todo.id
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")


async def update_by_id(todo_id: int, todo: UpdateTodoPayload):
    try:
        async with get_db() as db:
            db_todo = await db.execute(Todo).filter(Todo.id == todo_id).first()

            if todo.title:
                db_todo.title = todo.title
            if todo.description:
                db_todo.description = todo.description
            if todo.completed is not None:
                db_todo.completed = todo.completed
            if todo.ended is not None:
                db_todo.ended = todo.ended
            if todo.deleted is not None:
                db_todo.deleted = todo.deleted
            if todo.edited_at:
                db_todo.edited_at = todo.edited_at
            if todo.completed_at:
                db_todo.completed_at = todo.completed_at
            if todo.ending_at:
                db_todo.ending_at = todo.ending_at
            if todo.deleted_at:
                db_todo.deleted_at = todo.deleted_at

            await db.commit()
            return db_todo.id
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")


async def delete_by_id(todo_id: int):
    try:
        async with get_db() as db:
            todo = await db.execute(Todo).filter(Todo.id == todo_id).first()

            await db.delete(todo)
            await db.commit()
            return todo
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")
