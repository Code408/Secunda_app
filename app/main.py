from fastapi import FastAPI
from app.api.routers import router
from app.models import init_models
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация БД при старте
    await init_models()
    yield
    # Корректное закрытие соединений при завершении
    from app.db.session import async_engine
    await async_engine.dispose()

app = FastAPI(
    title="Secunda Organizations API",
    lifespan=lifespan
)

app.include_router(router)

