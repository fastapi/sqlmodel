import sqlalchemy as sa
from alembic import op


def upgrade():
    op.alter_column(
        "event",
        "created_at",
        existing_type=sa.DateTime(timezone=False),
        type_=sa.DateTime(timezone=True),
        postgresql_using="created_at AT TIME ZONE 'UTC'",
    )


def downgrade():
    op.alter_column(
        "event",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=sa.DateTime(timezone=False),
        postgresql_using="created_at AT TIME ZONE 'UTC'",
    )
