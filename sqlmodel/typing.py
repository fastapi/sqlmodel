from typing import Any, Optional

from pydantic import ConfigDict


class SQLModelConfig(ConfigDict, total=False):
    table: Optional[bool]
    read_from_attributes: Optional[bool]
    registry: Optional[Any]
