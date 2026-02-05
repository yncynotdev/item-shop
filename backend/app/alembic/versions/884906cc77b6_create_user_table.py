"""create user table

Revision ID: 884906cc77b6
Revises: 17951c949502
Create Date: 2026-01-29 07:55:47.352565

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '884906cc77b6'
down_revision: Union[str, Sequence[str], None] = '17951c949502'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("email", sa.String),
        sa.Column("name", sa.String)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
