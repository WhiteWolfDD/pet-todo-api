import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.main import get_db
from app.models.user import User
from app.schemas.user import UserPayload, UserResponse
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException


async def get_user_by_args(db: AsyncSession, user_args: int | str):
    if isinstance(user_args, int):
        user = await db.execute(select(UserResponse).filter(User.id == user_args))
        user = user.first()
    else:
        user = await db.execute(select(UserResponse).filter(User.username == user_args))
        user = user.first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_users(skip: int = 0, limit: int = 100):
    async with get_db() as db:
        try:
            result = await db.execute(select(User).offset(skip).limit(limit))
            users = result.scalars().all()
            return [UserResponse.model_validate(user) for user in users]
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Database error")


async def get_user(user_args: int | str):
    async with get_db() as db:
        try:
            user = await get_user_by_args(db, user_args)
            return UserResponse.model_validate(user)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Database error")


async def create_user(user: UserPayload):
    async with get_db() as db:
        try:
            db_user = User(
                username=user.username,
                password=bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
            )
            await db.add(db_user)
            await db.commit()
            return db_user.id
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Database error")


async def update_user(user_args: int | str, user: UserPayload):
    async with get_db() as db:
        try:
            db_user = await get_user_by_args(db, user_args)

            db_user.username = user.username
            db_user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            await db.commit()
            return db_user.id
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Database error")


async def delete_user(user_args: int | str):
    async with get_db() as db:
        try:
            user = await get_user_by_args(db, user_args)

            await db.delete(user)
            await db.commit()
            return user
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Database error")
