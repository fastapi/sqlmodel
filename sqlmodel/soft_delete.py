from datetime import datetime

from sqlmodel import Field


class SoftDeleteMixin:
    deleted_at: datetime | None = Field(default=None, nullable=True)
