from pydantic import ConfigDict
from typing import Optional, Any

class SQLModelConfig(ConfigDict):
    table: Optional[bool]
    read_from_attributes: Optional[bool]
    registry: Optional[Any]