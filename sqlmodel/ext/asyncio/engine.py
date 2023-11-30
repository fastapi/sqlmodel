from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine


# create_async_engine by default already has future set to be true.
# Porting this over to sqlmodel to make it easier to use.
def create_async_engine(*args: Any, **kwargs: Any) -> AsyncEngine:
    return _create_async_engine(*args, **kwargs)
