from fastapi import APIRouter

from app.controllers.user import *
from app.schemas.user import UserPayload

router = APIRouter()


@router.get("/users")
async def get(skip: int = 0, limit: int = 100):
    return await get_users(skip, limit)


@router.get("/users/{user_id}")
async def get_by_id(user_id: int):
    return await get_user(user_id)


@router.post("/users")
async def create(user: UserPayload):
    return await create_user(user)


@router.put("/users/{user_id}")
async def update(user_id: int, user: UserPayload):
    return await update_user(user_id, user)


@router.delete("/users/{user_id}")
async def delete(user_id: int):
    return await delete_user(user_id)
