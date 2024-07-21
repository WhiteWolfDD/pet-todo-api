import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

load_dotenv()

Base = declarative_base()

connect_args = {"check_same_thread": False} if os.getenv("DATABASE_URI").startswith("sqlite") else {}
engine = create_async_engine(os.getenv("DATABASE_URI"), connect_args=connect_args, pool_recycle=3600, echo=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_db():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
