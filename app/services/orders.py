from app.models import Order
from app.repositories.orders import OrderRepository
from sqlalchemy import Sequence
from app.schemas.order import OrderRequest


class OrderService:

    CACHE_TTL = 600

    def __init__(self, repository: OrderRepository):
        self.repository = repository

    @staticmethod
    def build_order_from_schema(data: OrderRequest) -> Order:
        return Order.model_validate(data)

    async def add_order(self, order: Order) -> Order:
        return await self.repository.add_order(order=order)

    async def get_order(self, order_id: int) -> Order:
        return await self.repository.get_order(order_id=order_id)

    async def get_orders(self, filters=None, order_by="id", order="asc") -> Sequence[Order]:
        return await self.repository.get_orders(filters=filters, order_by=order_by, order=order)

