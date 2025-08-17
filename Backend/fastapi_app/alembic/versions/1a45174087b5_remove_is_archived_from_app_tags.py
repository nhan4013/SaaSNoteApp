"""Remove is_archived from app_tags

Revision ID: 1a45174087b5
Revises: 06e523dee6d0
Create Date: 2025-08-14 20:55:15.126040

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a45174087b5'
down_revision: Union[str, Sequence[str], None] = '06e523dee6d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('app_tags', 'is_archived')
    op.add_column('app_notes', sa.Column('is_archived', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('app_notes', 'is_archived')
    op.add_column('app_tags', sa.Column('is_archived', sa.Boolean(), nullable=False, server_default=sa.false()))
