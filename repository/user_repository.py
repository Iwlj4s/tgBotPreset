from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

from dao.general_dao import GeneralDAO
from dao.tasks_dao import TasksDAO
from database import models, schema


async def add_user(user_tg_id: int,
                   user_name: str,
                   session: AsyncSession):
    print("ADD USER FUNC")
    user = await GeneralDAO.get_item_by_tg_id(item_tg_id=user_tg_id,
                                              item=models.User,
                                              session=session)

    if user:
        print("USER ALREADY EXIST")
        return {
            'message': "User already exist",
            'status_code': 409,
            'error': "CONFLICT"
        }

    print("CREATING USER")
    new_user = models.User(tg_id=user_tg_id, name=user_name)
    print(f"NEW USER: {new_user}")
    session.add(new_user)
    print("SESSION ADDED USER")
    await session.commit()
    print("SESSION COMMITED USER")
    await session.refresh(new_user)
    print("SESSION REFRESHED USER")

    return {
        'message': "User created successfully",
        'status_code': 201,
        'status': "success",
        'data': {
            'id': new_user.id,
            'tg_id': new_user.tg_id,
            'name': new_user.name,
            'created': new_user.created
        }
    }


async def add_task(data: dict,
                   session: AsyncSession):

    await TasksDAO.add_task(data=data, session=session)

    return {
        'message': "Task created successfully",
        'status_code': 201,
        'status': "success",
    }


async def close_task(data: dict,
                     old_task,
                     session: AsyncSession):
    await TasksDAO.add_closed_task(data=data, old_task=old_task, session=session)

    return {
        'message': "Task closed successfully",
        'status_code': 200,
        'status': "success",
    }


