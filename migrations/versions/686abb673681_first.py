"""first

Revision ID: 686abb673681
Revises: 
Create Date: 2025-03-28 23:33:13.692288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '686abb673681'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def _create_su():
    from datetime import datetime as dt
    from app.config import AppConfig as ac
    from uuid import uuid4

    base_gen = lambda: {'id': str(uuid4()), 'created_at': dt.now(), 'updated_at': dt.now()}
    s_users = [{**base_gen(), 'is_superuser': True, 'is_active': True, 'email': i} for i in ac.su_default_emails]

    meta = sa.MetaData()
    bind = op.get_bind()
    op.bulk_insert(sa.Table('user', meta, autoload_with=bind), s_users)

def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('audio',
    sa.Column('name', sa.String(length=512), nullable=False),
    sa.Column('path', sa.String(length=1024), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

    _create_su()




def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('audio')
    op.drop_table('user')
    # ### end Alembic commands ###
