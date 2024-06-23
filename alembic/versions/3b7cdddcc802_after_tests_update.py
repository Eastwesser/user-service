"""after tests update

Revision ID: 3b7cdddcc802
Revises: 0de3c8d0621c
Create Date: 2024-06-23 19:04:41.871911

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b7cdddcc802'
down_revision: Union[str, None] = '0de3c8d0621c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
