from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
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
    description="""
    API для справочника организаций с геолокацией и видами деятельности
    
    Основные возможности:
    - Поиск организаций по различным критериям
    - Иерархическая система видов деятельности (до 3 уровней)
    - Геопоиск организаций в заданном радиусе
    - Полнотекстовый поиск по названию
    
    Доступны два интерфейса:
    - HTML интерфейс для пользователей (web/organizations/)
    - JSON ответы (organizations/)
    """,
    version="1.0.0",
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[{
        "name": "organizations",
        "description": "Операции с организациями",
    }],
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    lifespan=lifespan
)

# Mount static files for documentation assets
# app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)
