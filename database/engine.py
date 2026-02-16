import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.models import Base

from config import Settings

current_db_url = Settings.CURRENT_DB_URL

engine = create_async_engine(current_db_url, echo=True,
                             future=True,     # Use new SQLAlchemy 2.0 features
                             pool_pre_ping=True,  # Check connection before use  
                             pool_recycle=300,    # Reconnect every 300 seconds 
                             )
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
