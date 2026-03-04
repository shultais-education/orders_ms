from typing import Annotated, TypeAlias
from app.models.order import Order
from app.repositories.orders import OrderRepository
from app.services.orders import OrderService
from fastapi import Depends
from app.api.dependencies.database import DBSessionDep


def get_order_repository(session: DBSessionDep) -> OrderRepository:
    return OrderRepository(session=session, model=Order)


OrderRepositoryDep: TypeAlias = Annotated[OrderRepository, Depends(get_order_repository)]


def get_order_service(repository: OrderRepositoryDep) -> OrderService:
    return OrderService(repository=repository)


OrderServiceDep: TypeAlias = Annotated[OrderService, Depends(get_order_service)]
