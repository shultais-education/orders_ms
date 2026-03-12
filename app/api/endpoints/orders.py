from fastapi import APIRouter
from fastapi import HTTPException
from typing import List
from app.core.config import settings

from app.schemas.order import OrderRequest, OrderDetail, Order
from app.api.dependencies.orders import OrderServiceDep
from app.api.dependencies.http_client import HTTPClientDep
from app.api.dependencies.security import JWTDep


orders_router = APIRouter(prefix="/orders", tags=["orders"])


@orders_router.get("", response_model=List[OrderDetail], summary="Возвращает заказы", description="Возвращает список заказов")
async def get_orders(order_service: OrderServiceDep):
    return await order_service.get_orders()


@orders_router.post("", response_model=OrderDetail, summary="Создание заказа")
async def add_order(jwt: JWTDep, order: OrderRequest, order_service: OrderServiceDep, http_client: HTTPClientDep):

    house_info_response = await http_client.get(f"{settings.HOUSE_INFO_ENDPOINT}/{order.house_id}")

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

    user_info_response = await http_client.get(
        f"{settings.USER_INFO_ENDPOINT}/{jwt['user_id']}",
        headers={"X-API-Key": settings.AUTH_API_KEY}
    )

    if user_info_response.status_code == 200:
        user_info = user_info_response.json()
    elif user_info_response.status_code == 404:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": ["body"],
                    "msg": f"Пользователь {jwt['user_id']} не найден",
                    "type": "value_error.user_not_found"
                }]
        )
    else:
        raise HTTPException(house_info_response.status_code, detail=[{}])

    emails = list()

    emails.append({
        "subject": f"Новая заявка на дом {house_info['name']}",
        "text": f"Вам поступила новая заявка на дома {house_info['name']} от пользователя {user_info['first_name']}.",
        "to": f"{order.house_id}-manger@example.com",
        "delay": 0
    })

    emails.append({
        "subject": f"Вы забронировали дом {house_info['name']}",
        "text": f"Здравствуйте, {user_info['first_name']}!\n\nВы успешно забронировали дом {house_info['name']}.",
        "to": user_info['email'],
        "delay": 0
    })

    sender_response = await http_client.post(
        settings.MESSAGES_ENDPOINT, json=emails, headers={"X-API-Key": settings.SENDER_API_KEY})
    if sender_response.status_code != 202:
        print(sender_response.json())

    order = order_service.build_order_from_schema(Order(**{
        "house_id": order.house_id,
        "user_name": user_info['first_name'],
        "user_email": user_info['email'],
    }).model_dump())
    order = await order_service.add_order(order)
    return order
