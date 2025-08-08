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

# Alembic config
config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

# Фильтр для системных схем MySQL
def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and object.schema in ['mysql', 'performance_schema', 'information_schema', 'sys']:
        return False
    elif type_ == "column" and object.table.schema in ['mysql', 'performance_schema', 'information_schema', 'sys']:
        return False
    return True

# 💡 Функция для подмены async URL на sync URL
def get_sync_url():
    url = os.getenv("DATABASE_URL")
    return url.replace("mysql+aiomysql", "mysql+pymysql")

# OFFLINE режим
def run_migrations_offline():
    url = get_sync_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# ONLINE режим
def run_migrations_online():
    from sqlalchemy import create_engine

    connectable = create_engine(get_sync_url(), pool_pre_ping=True)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            include_schemas=True,
            include_object=include_object,
            render_as_batch=True
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
