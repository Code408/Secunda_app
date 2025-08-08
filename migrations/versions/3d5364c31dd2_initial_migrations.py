from alembic import op
import sqlalchemy as sa

revision = '3d5364c31dd2'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # создание таблиц (как у тебя есть)
    op.create_table('activities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('level', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['parent_id'], ['activities.id']),
        sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('activities', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_activities_id'), ['id'], unique=False)

    op.create_table('buildings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('address', sa.String(length=255), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('address')
    )
    with op.batch_alter_table('buildings', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_buildings_id'), ['id'], unique=False)

    op.create_table('organizations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('building_id', sa.Integer(), nullable=False),
        sa.Column('phones', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['building_id'], ['buildings.id']),
        sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('organizations', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_organizations_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_organizations_name'), ['name'], unique=False)

    op.create_table('organization_activities',
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.Column('activity_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['activity_id'], ['activities.id']),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id']),
        sa.PrimaryKeyConstraint('organization_id', 'activity_id')
    )

    # Вставка данных через op.execute()

    # Данные activities
    op.execute("""
        INSERT INTO activities (id, name, parent_id, level) VALUES
        (1, 'Еда', NULL, 1),
        (2, 'Мясная продукция', 1, 2),
        (3, 'Молочная продукция', 1, 2),
        (4, 'Автомобили', NULL, 1),
        (5, 'Грузовые', 4, 2),
        (6, 'Легковые', 4, 2),
        (7, 'Запчасти', 6, 3),
        (8, 'Аксессуары', 6, 3)
    """)

    # Данные buildings
    op.execute("""
        INSERT INTO buildings (id, address, latitude, longitude) VALUES
        (1, 'г. Москва, ул. Ленина 1, офис 3', 55.755826, 37.617300),
        (2, 'г. Москва, ул. Блюхера 32/1', 55.762863, 37.608521),
        (3, 'г. Москва, ул. Тверская 10', 55.757989, 37.611523)
    """)

    # Данные organizations
    op.execute("""
        INSERT INTO organizations (id, name, building_id, phones) VALUES
        (1, 'ООО "Рога и Копыта"', 1, '["2-222-222", "3-333-333"]'),
        (2, 'Молочные продукты "Деревенька"', 2, '["8-800-555-3535"]'),
        (3, 'Автозапчасти "Колесо"', 3, '["8-495-123-4567"]')
    """)

    # Связи organization_activities
    op.execute("""
        INSERT INTO organization_activities (organization_id, activity_id) VALUES
        (1, 2),
        (1, 3),
        (2, 3),
        (3, 7)
    """)


def downgrade():
    # Удаляем данные из таблиц в обратном порядке (опционально)
    op.execute("DELETE FROM organization_activities")
    op.execute("DELETE FROM organizations")
    op.execute("DELETE FROM buildings")
    op.execute("DELETE FROM activities")

    # Далее удаляем таблицы (как у тебя есть)
    op.drop_table('organization_activities')
    with op.batch_alter_table('organizations', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_organizations_name'))
        batch_op.drop_index(batch_op.f('ix_organizations_id'))
    op.drop_table('organizations')
    with op.batch_alter_table('buildings', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_buildings_id'))
    op.drop_table('buildings')
    with op.batch_alter_table('activities', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_activities_id'))
    op.drop_table('activities')
