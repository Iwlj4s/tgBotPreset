from sqlalchemy import select, update, delete, and_, func, desc

from sqlalchemy.ext.asyncio import AsyncSession

from database import models


class TasksDAO:
    @classmethod
    async def add_task(cls, session: AsyncSession, data: dict):
        obj = models.Task(
            user_id=data["user_id"],
            task_name=data["task_name"],
            task_body=data["task_body"]
        )

        session.add(obj)

        await session.commit()

    @classmethod
    async def add_closed_task(cls, session: AsyncSession, data, old_task):
        obj = models.ClosedTask(
            task_id=data.id,
            user_id=data.user_id,
            task_name=data.task_name,
            task_body=data.task_body
        )

        session.add(obj)
        await session.delete(old_task)
        await session.commit()

    @classmethod
    async def get_tasks_by_user_id(cls, session: AsyncSession, user_id: int):
        query = select(models.Task).where(models.Task.user_id == user_id)
        items = await session.execute(query)

        return items.scalars().all()

    @classmethod
    async def get_closed_tasks_by_user_id(cls, session: AsyncSession, user_id: int):
        query = select(models.ClosedTask).where(models.ClosedTask.user_id == user_id)
        items = await session.execute(query)

        return items.scalars().all()
    
    @classmethod
    async def get_task_by_user_id(cls, session: AsyncSession, user_id: int, task_id: int):
        query = select(models.Task).where(models.Task.user_id == user_id,
                                          models.Task.id == task_id)
        
        task = await session.execute(query)

        return task.scalar_one_or_none()
