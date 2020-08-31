"""v0.4.0

Revision ID: 432e3447c36b
Revises: 
Create Date: 2020-08-24 18:59:50.823614

"""
from alembic import op
import geoalchemy2
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '432e3447c36b'
down_revision = None
branch_labels = ('bdc_catalog',)
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('applications',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('version', sa.String(length=32), nullable=False),
    sa.Column('uri', sa.String(length=255), nullable=True),
    sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True, comment='Follow the JSONSchema @jsonschemas/application-metadata.json'),
    sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.Column('updated', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.PrimaryKeyConstraint('id', name=op.f('applications_pkey')),
    sa.UniqueConstraint('name', 'version', name=op.f('applications_name_key')),
    schema='bdc'
    )
    op.create_table('composite_functions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('alias', sa.String(length=6), nullable=False),
    sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.Column('updated', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.PrimaryKeyConstraint('id', name=op.f('composite_functions_pkey')),
    sa.UniqueConstraint('alias', name=op.f('composite_functions_alias_key')),
    sa.UniqueConstraint('name', name=op.f('composite_functions_name_key')),
    schema='bdc'
    )
    op.create_table('grid_ref_sys',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('table_id', postgresql.OID(), nullable=False),
    sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.Column('updated', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.PrimaryKeyConstraint('id', name=op.f('grid_ref_sys_pkey')),
    sa.UniqueConstraint('name', name=op.f('grid_ref_sys_name_key')),
    schema='bdc'
    )
    op.create_table('mime_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.Column('updated', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.PrimaryKeyConstraint('id', name=op.f('mime_type_pkey')),
    sa.UniqueConstraint('name', name=op.f('mime_type_name_key')),
    schema='bdc'
    )
    op.create_table('providers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('uri', sa.String(length=255), nullable=True),
    sa.Column('credentials', postgresql.JSONB(astext_type=sa.Text()), nullable=True, comment='Follow the JSONSchema @jsonschemas/provider-credentials.json'),
    sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.Column('updated', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.PrimaryKeyConstraint('id', name=op.f('providers_pkey')),
    schema='bdc'
    )
    op.create_index(op.f('idx_bdc_providers_name'), 'providers', ['name'], unique=False, schema='bdc')
    op.create_table('resolution_unit',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('symbol', sa.String(length=3), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.Column('updated', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.PrimaryKeyConstraint('id', name=op.f('resolution_unit_pkey')),
    sa.UniqueConstraint('name', name=op.f('resolution_unit_name_key')),
    schema='bdc'
    )
    op.create_table('collections',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False, comment='Collection name internally.'),
    sa.Column('title', sa.String(length=255), nullable=False, comment='A human-readable string naming for collection.'),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('temporal_composition_schema', postgresql.JSONB(astext_type=sa.Text()), nullable=True, comment='Follow the JSONSchema @jsonschemas/collection-temporal-composition-schema.json'),
    sa.Column('composite_function_id', sa.Integer(), nullable=True, comment='Function schema identifier. Used for data cubes.'),
    sa.Column('grid_ref_sys_id', sa.Integer(), nullable=True),
    sa.Column('collection_type', sa.Enum('cube', 'collection', name='collection_type'), nullable=False),
    sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True, comment='Follow the JSONSchema @jsonschemas/collection-metadata.json'),
    sa.Column('is_public', sa.Boolean(), nullable=False),
    sa.Column('start_date', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('end_date', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('extent', geoalchemy2.types.Geometry(geometry_type='POLYGON', srid=4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('version', sa.String(length=3), nullable=False),
    sa.Column('version_predecessor', sa.Integer(), nullable=True),
    sa.Column('version_successor', sa.Integer(), nullable=True),
    sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.Column('updated', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.ForeignKeyConstraint(['composite_function_id'], ['bdc.composite_functions.id'], name=op.f('collections_composite_function_id_composite_functions_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['grid_ref_sys_id'], ['bdc.grid_ref_sys.id'], name=op.f('collections_grid_ref_sys_id_grid_ref_sys_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['version_predecessor'], ['bdc.collections.id'], name=op.f('collections_version_predecessor_collections_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['version_successor'], ['bdc.collections.id'], name=op.f('collections_version_successor_collections_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('collections_pkey')),
    sa.UniqueConstraint('name', 'version', name=op.f('collections_name_key')),
    schema='bdc'
    )
    op.create_index(op.f('idx_bdc_collections_extent'), 'collections', ['extent'], unique=False, schema='bdc', postgresql_using='gist')
    op.create_index(op.f('idx_bdc_collections_grid_ref_sys_id'), 'collections', ['grid_ref_sys_id'], unique=False, schema='bdc')
    op.create_index(op.f('idx_bdc_collections_name'), 'collections', ['name'], unique=False, schema='bdc')
    op.create_table('tiles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('grid_ref_sys_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.Column('updated', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.ForeignKeyConstraint(['grid_ref_sys_id'], ['bdc.grid_ref_sys.id'], name=op.f('tiles_grid_ref_sys_id_grid_ref_sys_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('tiles_pkey')),
    schema='bdc'
    )
    op.create_index(op.f('idx_bdc_tiles_grid_ref_sys_id'), 'tiles', ['grid_ref_sys_id'], unique=False, schema='bdc')
    op.create_index(op.f('idx_bdc_tiles_id'), 'tiles', ['id'], unique=False, schema='bdc')
    op.create_index(op.f('idx_bdc_tiles_name'), 'tiles', ['name'], unique=False, schema='bdc')
    op.create_table('bands',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('common_name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('min_value', sa.Numeric(), nullable=True),
    sa.Column('max_value', sa.Numeric(), nullable=True),
    sa.Column('nodata', sa.Numeric(), nullable=True),
    sa.Column('scale', sa.Numeric(), nullable=True),
    sa.Column('resolution_x', sa.Numeric(), nullable=True),
    sa.Column('resolution_y', sa.Numeric(), nullable=True),
    sa.Column('center_wavelength', sa.Numeric(), nullable=True),
    sa.Column('full_width_half_max', sa.Numeric(), nullable=True),
    sa.Column('collection_id', sa.Integer(), nullable=True),
    sa.Column('resolution_unit_id', sa.Integer(), nullable=True),
    sa.Column('data_type', sa.Enum('uint8', 'int8', 'uint16', 'int16', 'uint32', 'int32', 'float32', 'float64', name='data_type'), nullable=True),
    sa.Column('mime_type_id', sa.Integer(), nullable=True),
    sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True, comment='Follow the JSONSchema @jsonschemas/band-metadata.json'),
    sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.Column('updated', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.ForeignKeyConstraint(['collection_id'], ['bdc.collections.id'], name=op.f('bands_collection_id_collections_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['mime_type_id'], ['bdc.mime_type.id'], name=op.f('bands_mime_type_id_mime_type_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['resolution_unit_id'], ['bdc.resolution_unit.id'], name=op.f('bands_resolution_unit_id_resolution_unit_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('bands_pkey')),
    schema='bdc'
    )
    op.create_index(op.f('idx_bdc_bands_collection_id'), 'bands', ['collection_id'], unique=False, schema='bdc')
    op.create_index(op.f('idx_bdc_bands_common_name'), 'bands', ['common_name'], unique=False, schema='bdc')
    op.create_index(op.f('idx_bdc_bands_mime_type_id'), 'bands', ['mime_type_id'], unique=False, schema='bdc')
    op.create_index(op.f('idx_bdc_bands_name'), 'bands', ['name'], unique=False, schema='bdc')
    op.create_table('collection_src',
    sa.Column('collection_id', sa.Integer(), nullable=False),
    sa.Column('collection_src_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.Column('updated', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.ForeignKeyConstraint(['collection_id'], ['bdc.collections.id'], name=op.f('collection_src_collection_id_collections_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['collection_src_id'], ['bdc.collections.id'], name=op.f('collection_src_collection_src_id_collections_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('collection_id', 'collection_src_id', name=op.f('collection_src_pkey')),
    schema='bdc'
    )
    op.create_table('collections_providers',
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.Column('collection_id', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('priority', sa.SmallInteger(), nullable=False),
    sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.Column('updated', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.ForeignKeyConstraint(['collection_id'], ['bdc.collections.id'], name=op.f('collections_providers_collection_id_collections_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['provider_id'], ['bdc.providers.id'], name=op.f('collections_providers_provider_id_providers_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('provider_id', 'collection_id', name=op.f('collections_providers_pkey')),
    schema='bdc'
    )
    op.create_table('items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('collection_id', sa.Integer(), nullable=False),
    sa.Column('tile_id', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('end_date', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('cloud_cover', sa.Numeric(), nullable=True),
    sa.Column('assets', postgresql.JSONB(astext_type=sa.Text()), nullable=True, comment='Follow the JSONSchema @jsonschemas/item-assets.json'),
    sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True, comment='Follow the JSONSchema @jsonschemas/item-metadata.json'),
    sa.Column('provider_id', sa.Integer(), nullable=True),
    sa.Column('application_id', sa.Integer(), nullable=True),
    sa.Column('geom', geoalchemy2.types.Geometry(geometry_type='POLYGON', srid=4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('min_convex_hull', geoalchemy2.types.Geometry(geometry_type='POLYGON', srid=4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('srid', sa.Integer(), nullable=True),
    sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.Column('updated', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.ForeignKeyConstraint(['application_id'], ['bdc.applications.id'], name=op.f('items_application_id_applications_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['collection_id'], ['bdc.collections.id'], name=op.f('items_collection_id_collections_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['provider_id'], ['bdc.providers.id'], name=op.f('items_provider_id_providers_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['srid'], ['public.spatial_ref_sys.srid'], name=op.f('items_srid_spatial_ref_sys_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tile_id'], ['bdc.tiles.id'], name=op.f('items_tile_id_tiles_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('items_pkey')),
    schema='bdc'
    )
    op.create_index(op.f('idx_bdc_items_cloud_cover'), 'items', ['cloud_cover'], unique=False, schema='bdc')
    op.create_index(op.f('idx_bdc_items_collection_id'), 'items', ['collection_id'], unique=False, schema='bdc')
    op.create_index(op.f('idx_bdc_items_geom'), 'items', ['geom'], unique=False, schema='bdc', postgresql_using='gist')
    op.create_index(op.f('idx_bdc_items_min_convex_hull'), 'items', ['min_convex_hull'], unique=False, schema='bdc', postgresql_using='gist')
    op.create_index(op.f('idx_bdc_items_name'), 'items', ['name'], unique=False, schema='bdc')
    op.create_index(op.f('idx_bdc_items_provider_id'), 'items', ['provider_id'], unique=False, schema='bdc')
    op.create_index(op.f('idx_bdc_items_start_date'), 'items', [sa.text('start_date DESC')], unique=False, schema='bdc')
    op.create_index(op.f('idx_bdc_items_tile_id'), 'items', ['tile_id'], unique=False, schema='bdc')
    op.create_index('idx_items_start_date_end_date', 'items', ['start_date', 'end_date'], unique=False, schema='bdc')
    op.create_table('quicklook',
    sa.Column('collection_id', sa.Integer(), nullable=False),
    sa.Column('red', sa.Integer(), nullable=True),
    sa.Column('green', sa.Integer(), nullable=True),
    sa.Column('blue', sa.Integer(), nullable=True),
    sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.Column('updated', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.ForeignKeyConstraint(['blue'], ['bdc.bands.id'], name=op.f('quicklook_blue_bands_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['collection_id'], ['bdc.collections.id'], name=op.f('quicklook_collection_id_collections_fkey')),
    sa.ForeignKeyConstraint(['green'], ['bdc.bands.id'], name=op.f('quicklook_green_bands_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['red'], ['bdc.bands.id'], name=op.f('quicklook_red_bands_fkey'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('collection_id', name=op.f('quicklook_pkey')),
    schema='bdc'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quicklook', schema='bdc')
    op.drop_index('idx_items_start_date_end_date', table_name='items', schema='bdc')
    op.drop_index(op.f('idx_bdc_items_tile_id'), table_name='items', schema='bdc')
    op.drop_index(op.f('idx_bdc_items_start_date'), table_name='items', schema='bdc')
    op.drop_index(op.f('idx_bdc_items_provider_id'), table_name='items', schema='bdc')
    op.drop_index(op.f('idx_bdc_items_name'), table_name='items', schema='bdc')
    op.drop_index(op.f('idx_bdc_items_min_convex_hull'), table_name='items', schema='bdc')
    op.drop_index(op.f('idx_bdc_items_geom'), table_name='items', schema='bdc')
    op.drop_index(op.f('idx_bdc_items_collection_id'), table_name='items', schema='bdc')
    op.drop_index(op.f('idx_bdc_items_cloud_cover'), table_name='items', schema='bdc')
    op.drop_table('items', schema='bdc')
    op.drop_table('collections_providers', schema='bdc')
    op.drop_table('collection_src', schema='bdc')
    op.drop_index(op.f('idx_bdc_bands_name'), table_name='bands', schema='bdc')
    op.drop_index(op.f('idx_bdc_bands_mime_type_id'), table_name='bands', schema='bdc')
    op.drop_index(op.f('idx_bdc_bands_common_name'), table_name='bands', schema='bdc')
    op.drop_index(op.f('idx_bdc_bands_collection_id'), table_name='bands', schema='bdc')
    op.drop_table('bands', schema='bdc')
    op.drop_index(op.f('idx_bdc_tiles_name'), table_name='tiles', schema='bdc')
    op.drop_index(op.f('idx_bdc_tiles_id'), table_name='tiles', schema='bdc')
    op.drop_index(op.f('idx_bdc_tiles_grid_ref_sys_id'), table_name='tiles', schema='bdc')
    op.drop_table('tiles', schema='bdc')
    op.drop_index(op.f('idx_bdc_collections_name'), table_name='collections', schema='bdc')
    op.drop_index(op.f('idx_bdc_collections_grid_ref_sys_id'), table_name='collections', schema='bdc')
    op.drop_index(op.f('idx_bdc_collections_extent'), table_name='collections', schema='bdc')
    op.drop_table('collections', schema='bdc')
    op.drop_table('resolution_unit', schema='bdc')
    op.drop_index(op.f('idx_bdc_providers_name'), table_name='providers', schema='bdc')
    op.drop_table('providers', schema='bdc')
    op.drop_table('mime_type', schema='bdc')
    op.drop_table('grid_ref_sys', schema='bdc')
    op.drop_table('composite_functions', schema='bdc')
    op.drop_table('applications', schema='bdc')
    # ### end Alembic commands ###
