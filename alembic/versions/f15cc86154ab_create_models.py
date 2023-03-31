"""Create models

Revision ID: f15cc86154ab
Revises: 
Create Date: 2023-02-21 22:02:12.252310

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f15cc86154ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('user')
    # op.drop_table('church')
    # op.drop_table('rol')
    # op.drop_table('detachment')
    # op.drop_table('subdetachment')
    #op.drop_table('city')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('city',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('city_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('postal_code', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='city_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('subdetachment',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('image', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('detachment_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['detachment_id'], ['detachment.id'], name='subdetachment_detachment_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='subdetachment_pkey')
    )
    op.create_table('detachment',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('section', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('numbers', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('district', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('church_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['church_id'], ['church.id'], name='detachment_church_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='detachment_pkey')
    )
    op.create_table('rol',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('rol_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='rol_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('church',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('church_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('telephone', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='church_pkey'),
    sa.UniqueConstraint('email', name='church_email_key'),
    sa.UniqueConstraint('name', name='church_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('image', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('identification', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('type_identification', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('birth_day', sa.VARCHAR(length=12), autoincrement=False, nullable=True),
    sa.Column('birth_place', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('gender', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('rh', sa.VARCHAR(length=6), autoincrement=False, nullable=True),
    sa.Column('direction', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('phone_number', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('cell_phone', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('civil_status', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('position', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('occupation', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('school', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('grade', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('hobbies_interests', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('allergies', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('baptism_water', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('baptism_spirit', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('year_conversion', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('rol_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('church_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('city_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('ceated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['church_id'], ['church.id'], name='user_church_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['city_id'], ['city.id'], name='user_city_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['rol_id'], ['rol.id'], name='user_rol_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key'),
    sa.UniqueConstraint('username', name='user_username_key')
    )
    # ### end Alembic commands ###
