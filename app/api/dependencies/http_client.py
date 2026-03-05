from typing import Annotated, TypeAlias
from typing import AsyncGenerator

from fastapi import Depends
from httpx import AsyncClient


async def get_async_client() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient() as client:
        yield client


HTTPClientDep: TypeAlias = Annotated[AsyncClient, Depends(get_async_client)]
