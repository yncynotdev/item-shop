"""create item table

Revision ID: ccf4946e402d
Revises: 
Create Date: 2026-01-17 17:27:49.941489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ccf4946e402d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('types', sa.String, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('img', sa.String, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('items')
