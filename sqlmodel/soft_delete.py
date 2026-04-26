from datetime import datetime
from typing import Optional

from sqlmodel import Field


class SoftDeleteMixin:
    """
    Mixin that adds a `deleted_at` timestamp column.

    Usage:
        class MyModel(SQLModel, SoftDeleteMixin, table=True): ...
    """
    deleted_at: Optional[datetime] = Field(default=None)