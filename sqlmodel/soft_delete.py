from datetime import datetime

from sqlmodel import Field


class SoftDeleteMixin:
    """
    Mixin that adds a `deleted_at` timestamp column.

    Usage:
        class MyModel(SQLModel, SoftDeleteMixin, table=True): ...
    """

    deleted_at: datetime | None = Field(default=None)
