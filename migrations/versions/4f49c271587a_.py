"""empty message

Revision ID: 4f49c271587a
Revises: 5c12f3ec5a1d
Create Date: 2024-09-22 17:32:50.104823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f49c271587a'
down_revision = '5c12f3ec5a1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('especies', sa.String(length=250), nullable=False),
    sa.Column('role', sa.String(length=250), nullable=False),
    sa.Column('lifestatus', sa.String(length=250), nullable=False),
    sa.Column('gender', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('galactic_location', sa.String(length=250), nullable=False),
    sa.Column('climate', sa.String(length=40), nullable=False),
    sa.Column('population', sa.String(length=40), nullable=False),
    sa.Column('native_species', sa.String(length=40), nullable=False),
    sa.Column('govemment', sa.String(length=40), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('character_fav_view',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planet_fav_view',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('favorites_planets')
    op.drop_table('planets')
    op.drop_table('characters')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('especies', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('role', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('lifestatus', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('gender', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='characters_pkey'),
    sa.UniqueConstraint('name', name='characters_name_key')
    )
    op.create_table('planets',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('planets_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('galactic_location', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('climate', sa.VARCHAR(length=40), autoincrement=False, nullable=False),
    sa.Column('population', sa.VARCHAR(length=40), autoincrement=False, nullable=False),
    sa.Column('native_species', sa.VARCHAR(length=40), autoincrement=False, nullable=False),
    sa.Column('govemment', sa.VARCHAR(length=40), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='planets_pkey'),
    sa.UniqueConstraint('name', name='planets_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('favorites_planets',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['planet_id'], ['planets.id'], name='favorites_planets_planet_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='favorites_planets_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'planet_id', name='favorites_planets_pkey')
    )
    op.drop_table('planet_fav_view')
    op.drop_table('character_fav_view')
    op.drop_table('planet')
    op.drop_table('character')
    # ### end Alembic commands ###
