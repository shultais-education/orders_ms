from fastapi import APIRouter
from typing import List


from app.schemas.order import OrderRequest, OrderDetail
from app.api.dependencies.orders import OrderServiceDep


orders_router = APIRouter(prefix="/orders", tags=["orders"])


@orders_router.get("", response_model=List[OrderDetail], summary="Возвращает заказы", description="Возвращает список заказов")
async def get_orders(order_service: OrderServiceDep):
    return await order_service.get_orders()


@orders_router.post("", response_model=OrderDetail, summary="Создание заказа")
async def add_order(order: OrderRequest, order_service: OrderServiceDep):
    order = order_service.build_order_from_schema(order)
    order = await order_service.add_order(order)
    return order
