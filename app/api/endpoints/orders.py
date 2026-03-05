from fastapi import APIRouter
from fastapi import HTTPException
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

    if house_info_response.status_code == 200:
        house_info = house_info_response.json()
    elif house_info_response.status_code == 404:
        raise HTTPException(
            status_code=422,
            detail=[{
                "loc": ["body", "house_id"],
                "msg": f"Дом {order.house_id} не найден или не активен",
                "type": "value_error.house_not_found"
            }]
        )
    else:
        raise HTTPException(house_info_response.status_code, detail=[{}])

    emails = list()

    emails.append({
        "subject": f"Новая заявка на дом {house_info['name']}",
        "text": f"Вам поступила новая заявка на дома {house_info['name']} от пользователя {order.user_name}.",
        "to": f"{order.house_id}-manger@example.com",
        "delay": 0
    })

    if order.user_email:
        emails.append({
            "subject": f"Вы забронировали дом {house_info['name']}",
            "text": f"Здравствуйте, {order.user_name}!\n\nВы успешно забронировали дом {house_info['name']}.",
            "to": order.user_email,
            "delay": 0
        })

    sender_response = await http_client.post(f"http://127.0.0.1:8010/messages", json=emails, headers={"X-API-Key": "ABC"})
    if sender_response.status_code != 202:
        print(sender_response.json())

    order = order_service.build_order_from_schema(order)
    order = await order_service.add_order(order)
    return order
