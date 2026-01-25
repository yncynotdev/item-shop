"""create new user

Revision ID: 4ca65161bb1f
Revises: ccf4946e402d
Create Date: 2026-01-23 21:30:52.142260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ca65161bb1f'
down_revision: Union[str, Sequence[str], None] = 'ccf4946e402d'
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
