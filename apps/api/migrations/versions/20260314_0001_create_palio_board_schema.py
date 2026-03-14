"""Create the baseline application schema."""

from alembic import op

APPLICATION_SCHEMA = "palio_board"
revision = "20260314_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create the empty application schema."""

    op.execute(f'CREATE SCHEMA IF NOT EXISTS "{APPLICATION_SCHEMA}"')


def downgrade() -> None:
    """Drop the empty application schema."""

    op.execute(f'DROP SCHEMA IF EXISTS "{APPLICATION_SCHEMA}" CASCADE')
