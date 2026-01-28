"""create image table

Revision ID: 2cc376f1f50c
Revises: 4ca65161bb1f
Create Date: 2026-01-27 22:46:59.054440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cc376f1f50c'
down_revision: Union[str, Sequence[str], None] = '4ca65161bb1f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "image",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("index_id", sa.Integer, nullable=False),
        sa.Column("url", sa.Integer, nullable=False)
    )

    op.drop_table("items")
    op.create_table(
        'items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('types', sa.String, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('image_id', sa.String, sa.ForeignKey(
            "image.index_id"), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("image")
    op.drop_table("items")
