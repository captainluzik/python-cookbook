from aiogram import types
from typing import Optional

from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, DateTime, func, select, insert, update, delete, literal_column,
    BigInteger
)

from settings import DATABASE_URI, LOCAL_MODE
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

Base = declarative_base()

engine: Optional[AsyncEngine] = None


async def init_database():
    global engine
    if LOCAL_MODE:
        DB_PATH = "/home/dmitriy/projects/deployment-planning-tool/db.sqlite3"
        engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}", echo=True)
    else:
        engine = create_async_engine(DATABASE_URI, echo=True)
    async with engine.begin() as conn:
        if LOCAL_MODE:
            await conn.run_sync(Base.metadata.create_all)
        else:
            pass


async def stop_database():
    if engine:
        await engine.dispose()
