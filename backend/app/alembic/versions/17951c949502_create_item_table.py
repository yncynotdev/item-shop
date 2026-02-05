"""create item table

Revision ID: 17951c949502
Revises: 
Create Date: 2026-01-29 07:51:14.079964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17951c949502'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'item',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('types', sa.String, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('image_url', sa.String, nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('item')
