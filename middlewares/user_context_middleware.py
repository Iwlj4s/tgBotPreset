from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TgUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import models
from context.request_context import RequestContext

class UserContextMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]) -> Any:
        
        # Session must be in data already using DataBaseSession
        session: AsyncSession = data.get('session')
        if not session:
            return await handler(event, data)

        tg_user: TgUser = data.get("event_from_user")
        if not tg_user:
            return await handler(event, data)

        # Search user by tg id (mb I'll use here something from DAO funcs)
        stmt = select(models.User).where(models.User.tg_id == tg_user.id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        created = False
        if not user:
            # Creating new user
            user = models.User(
                tg_id=tg_user.id,
                name=tg_user.full_name 
            )
            session.add(user)
            await session.flush()   # Get id without commit
            created = True
        elif user.name != tg_user.first_name:
            # Update name if it changed
            user.name = tg_user.first_name
            # Updates saving when handler has commit

        # If user just created - commit rightnow for get him saving even we have errors in handler 
        if created:
            await session.commit()

        # Formating context and use him in data
        context = RequestContext(session=session, current_user=user)
        data['request_context'] = context

        return await handler(event, data)