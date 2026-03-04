from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from sqlmodel import select, delete, desc, asc, and_
from typing import TypeVar, Type


DBModel = TypeVar("DBModel", bound=SQLModel)
PModel = TypeVar("PModel", bound=BaseModel)


class DBRepository:

    def __init__(self, model: Type[SQLModel], session: AsyncSession):
        self.model = model
        self.session = session

    async def create_one(self, obj: DBModel) -> DBModel:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update_one(self, obj: DBModel, data: PModel) -> DBModel:
        obj.sqlmodel_update(data.model_dump(exclude_unset=True))
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_one(self, id_: int):
        return await self.session.get(self.model, id_)

    async def get_many(self, filters=None, order_by="id", order="asc"):
        stmt = select(self.model)

        if filters:
            stmt = stmt.where(and_(*filters))

        ordering = desc if order == "desc" else asc
        stmt = stmt.order_by(ordering(order_by))

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_one(self, id_: int):
        stmt = delete(self.model).where(self.model.id == id_)
        await self.session.execute(stmt)
        await self.session.commit()
