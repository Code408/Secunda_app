from logging.config import fileConfig
from alembic import context
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app.models import Base
from app.models.organization import Organization
from app.models.building import Building
from app.models.activity import Activity

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def include_object(object, name, type_, reflected, compare_to):
    # Пропускаем системные схемы MySQL
    if type_ == "table" and object.schema in ['mysql', 'performance_schema', 'information_schema', 'sys']:
        return False
    # Для колонок проверяем схему родительской таблицы
    elif type_ == "column" and object.table.schema in ['mysql', 'performance_schema', 'information_schema', 'sys']:
        return False
    return True

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    from app.db.session import sync_engine
    
    with sync_engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            include_schemas=True,  # Важно для MySQL
            include_object=include_object,  # Добавляем наш фильтр
            render_as_batch=True  # Для совместимости с MySQL
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
