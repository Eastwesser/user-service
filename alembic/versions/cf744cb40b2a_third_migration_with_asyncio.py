"""Third migration with asyncio

Revision ID: cf744cb40b2a
Revises: 34709f6cf2a3
Create Date: 2024-06-19 11:22:32.647787

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf744cb40b2a'
down_revision: Union[str, None] = '34709f6cf2a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
