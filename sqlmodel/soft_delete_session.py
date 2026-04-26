from typing import Any

from sqlmodel.orm.session import Session

from sqlmodel.soft_delete import SoftDeleteMixin


class SoftDeleteSession(Session):
    def delete(self, instance: Any, hard_delete: bool = False) -> Any:
        if not hard_delete and isinstance(instance, SoftDeleteMixin):
            instance.deleted_at = self._now()
            self.add(instance)
            return instance
        return super().delete(instance)

    def _now(self) -> Any:
        from datetime import datetime, timezone
        return datetime.now(timezone.utc)