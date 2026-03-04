from app.models import Order
from app.repositories.db import DBRepository
from sqlalchemy import Sequence



class OrderRepository(DBRepository):

    async def add_order(self, order: Order) -> Order:
        return await self.create_one(obj=order)

    async def get_order(self, order_id: int) -> Order:
        return await self.get_one(id_=order_id)

    async def get_orders(self, filters=None, order_by="id", order="asc") -> Sequence[Order]:
        return await self.get_many(filters=filters, order_by=order_by, order=order)
