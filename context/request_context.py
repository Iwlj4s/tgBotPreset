from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from database import models

@dataclass
class RequestContext:
    session: AsyncSession
    current_user: models.User

