from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import Annotated, TypeAlias
from app.db.session import get_async_session


DBSessionDep: TypeAlias = Annotated[AsyncSession, Depends(get_async_session)]
