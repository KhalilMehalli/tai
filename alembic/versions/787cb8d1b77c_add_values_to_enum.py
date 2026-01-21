"""add values to enum

Revision ID: 787cb8d1b77c
Revises: f031d232305f
Create Date: 2026-01-17 16:37:59.807967

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '787cb8d1b77c'
down_revision: Union[str, Sequence[str], None] = 'f031d232305f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE language ADD VALUE IF NOT EXISTS 'JAVA'")
    op.execute("ALTER TYPE language ADD VALUE IF NOT EXISTS 'PYTHON'")
    op.execute("ALTER TYPE language ADD VALUE IF NOT EXISTS 'CCP'") 

    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
