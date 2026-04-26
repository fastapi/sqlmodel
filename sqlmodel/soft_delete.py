from datetime import datetime
from typing import Optional

from sqlmodel import Field


class SoftDeleteMixin:
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)