from fastapi import FastAPI
from app.api.endpoints.orders import orders_router
from contextlib import asynccontextmanager
from app.db.session import async_engine


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield

    await async_engine.dispose()


app = FastAPI(lifespan=lifespan, title="API заказов", description="Микросервис для управления заказами", root_path="/api")
app.include_router(orders_router)
