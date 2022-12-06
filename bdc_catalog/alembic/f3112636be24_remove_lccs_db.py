"""remove lccs-db

Revision ID: f3112636be24
Revises: 561ebe6266ad
Create Date: 2022-11-01 17:05:17.726004

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'f3112636be24'
down_revision = '5067fb4381c0'
branch_labels = ()
depends_on = None


def _has_column(table_name: str, column: str, schema: str = None) -> bool:
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind=bind)

    found_column = False
    for col in inspector.get_columns(table_name=table_name, schema=schema):
        if column in col['name']:
            found_column = True
            break

    return found_column


def upgrade():
    with op.batch_alter_table('collections', schema='bdc') as batch_op:
        if _has_column(table_name='collections', schema='bdc', column='classification_system_id'):
            batch_op.drop_column('classification_system_id')
        if not _has_column(table_name='collections', schema='bdc', column='is_public'):
            batch_op.add_column(sa.Column('is_public', sa.Boolean(), nullable=False, server_default='true'))
            batch_op.create_index(op.f('idx_bdc_collections_is_public'), ['is_public'], unique=False)

    op.create_index('idx_bdc_items_start_date_desc_id', 'items', [sa.text('start_date DESC'), 'id'], unique=False,
                    schema='bdc')
    op.create_index('idx_bdc_items_start_date_desc_id_is_available', 'items',
                    [sa.text('start_date DESC'), 'id', 'is_available'], unique=False,
                    schema='bdc')
    op.drop_table('collections_roles', schema='bdc')
    op.drop_table('roles', schema='bdc')
    # ### end Alembic commands ###


def downgrade():
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('roles_pkey')),
        sa.UniqueConstraint('name', name=op.f('roles_name_key')),
        schema='bdc'
    )
    op.create_index(op.f('idx_bdc_roles_name'), 'roles', ['name'], unique=False, schema='bdc')
    op.create_table(
        'collections_roles',
        sa.Column('collection_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['collection_id'], ['bdc.collections.id'],
                                name=op.f('collections_roles_collection_id_collections_fkey'), onupdate='CASCADE',
                                ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['role_id'], ['bdc.roles.id'], name=op.f('collections_roles_role_id_roles_fkey'),
                                onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('collection_id', 'role_id', name=op.f('collections_roles_pkey')),
        schema='bdc'
    )
    op.drop_index('idx_bdc_items_start_date_desc_id', table_name='items', schema='bdc')
    op.drop_index('idx_bdc_items_start_date_desc_id_is_available', table_name='items', schema='bdc')
