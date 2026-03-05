from fastapi import APIRouter
from typing import List


from app.schemas.order import OrderRequest, OrderDetail
from app.api.dependencies.orders import OrderServiceDep
from app.api.dependencies.http_client import HTTPClientDep


orders_router = APIRouter(prefix="/orders", tags=["orders"])


@orders_router.get("", response_model=List[OrderDetail], summary="Возвращает заказы", description="Возвращает список заказов")
async def get_orders(order_service: OrderServiceDep):
    return await order_service.get_orders()


@orders_router.post("", response_model=OrderDetail, summary="Создание заказа")
async def add_order(order: OrderRequest, order_service: OrderServiceDep, http_client: HTTPClientDep):

    house_info_response = await http_client.get(f"http://127.0.0.1:8000/houses/{order.house_id}")

    print(house_info_response.status_code)
    print(house_info_response.json())

    order = order_service.build_order_from_schema(order)
    order = await order_service.add_order(order)
    return order
