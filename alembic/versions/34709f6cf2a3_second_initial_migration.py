"""Second initial migration

Revision ID: 34709f6cf2a3
Revises: af60d735a810
Create Date: 2024-06-19 11:20:07.426247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34709f6cf2a3'
down_revision: Union[str, None] = 'af60d735a810'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
