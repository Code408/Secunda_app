from app.db.session import async_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Явно импортируем все модели
from .organization import Organization  # noqa
from .building import Building  # noqa
from .activity import Activity  # noqa

async def init_models():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Важно для Alembic
__all__ = ["Base", "Organization", "Building", "Activity"]