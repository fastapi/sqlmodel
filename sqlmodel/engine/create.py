import json
import sqlite3
from typing import Any, Callable, Dict, List, Optional, Type, Union

from sqlalchemy import create_engine as _create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.future import Engine as _FutureEngine
from sqlalchemy.pool import Pool
from typing_extensions import Literal, TypedDict

from ..default import Default, _DefaultPlaceholder

# Types defined in sqlalchemy2-stubs, but can't be imported, so re-define here

_Debug = Literal["debug"]

_IsolationLevel = Literal[
    "SERIALIZABLE",
    "REPEATABLE READ",
    "READ COMMITTED",
    "READ UNCOMMITTED",
    "AUTOCOMMIT",
]
_ParamStyle = Literal["qmark", "numeric", "named", "format", "pyformat"]
_ResetOnReturn = Literal["rollback", "commit"]


class _SQLiteConnectArgs(TypedDict, total=False):
    timeout: float
    detect_types: Any
    isolation_level: Optional[Literal["DEFERRED", "IMMEDIATE", "EXCLUSIVE"]]
    check_same_thread: bool
    factory: Type[sqlite3.Connection]
    cached_statements: int
    uri: bool


_ConnectArgs = Union[_SQLiteConnectArgs, Dict[str, Any]]


# Re-define create_engine to have by default future=True, and assume that's what is used
# Also show the default values used for each parameter, but don't set them unless
# explicitly passed as arguments by the user to prevent errors. E.g. SQLite doesn't
# support pool connection arguments.
def create_engine(
    url: Union[str, URL],
    *,
    connect_args: _ConnectArgs = Default({}),  # type: ignore
    echo: Union[bool, _Debug] = Default(False),
    echo_pool: Union[bool, _Debug] = Default(False),
    enable_from_linting: bool = Default(True),
    encoding: str = Default("utf-8"),
    execution_options: Dict[Any, Any] = Default({}),
    future: bool = True,
    hide_parameters: bool = Default(False),
    implicit_returning: bool = Default(True),
    isolation_level: Optional[_IsolationLevel] = Default(None),
    json_deserializer: Callable[..., Any] = Default(json.loads),
    json_serializer: Callable[..., Any] = Default(json.dumps),
    label_length: Optional[int] = Default(None),
    logging_name: Optional[str] = Default(None),
    max_identifier_length: Optional[int] = Default(None),
    max_overflow: int = Default(10),
    module: Optional[Any] = Default(None),
    paramstyle: Optional[_ParamStyle] = Default(None),
    pool: Optional[Pool] = Default(None),
    poolclass: Optional[Type[Pool]] = Default(None),
    pool_logging_name: Optional[str] = Default(None),
    pool_pre_ping: bool = Default(False),
    pool_size: int = Default(5),
    pool_recycle: int = Default(-1),
    pool_reset_on_return: Optional[_ResetOnReturn] = Default("rollback"),
    pool_timeout: float = Default(30),
    pool_use_lifo: bool = Default(False),
    plugins: Optional[List[str]] = Default(None),
    query_cache_size: Optional[int] = Default(None),
    **kwargs: Any,
) -> _FutureEngine:
    current_kwargs: Dict[str, Any] = {
        "future": future,
    }
    if not isinstance(echo, _DefaultPlaceholder):
        current_kwargs["echo"] = echo
    if not isinstance(echo_pool, _DefaultPlaceholder):
        current_kwargs["echo_pool"] = echo_pool
    if not isinstance(enable_from_linting, _DefaultPlaceholder):
        current_kwargs["enable_from_linting"] = enable_from_linting
    if not isinstance(connect_args, _DefaultPlaceholder):
        current_kwargs["connect_args"] = connect_args
    if not isinstance(encoding, _DefaultPlaceholder):
        current_kwargs["encoding"] = encoding
    if not isinstance(execution_options, _DefaultPlaceholder):
        current_kwargs["execution_options"] = execution_options
    if not isinstance(hide_parameters, _DefaultPlaceholder):
        current_kwargs["hide_parameters"] = hide_parameters
    if not isinstance(implicit_returning, _DefaultPlaceholder):
        current_kwargs["implicit_returning"] = implicit_returning
    if not isinstance(isolation_level, _DefaultPlaceholder):
        current_kwargs["isolation_level"] = isolation_level
    if not isinstance(json_deserializer, _DefaultPlaceholder):
        current_kwargs["json_deserializer"] = json_deserializer
    if not isinstance(json_serializer, _DefaultPlaceholder):
        current_kwargs["json_serializer"] = json_serializer
    if not isinstance(label_length, _DefaultPlaceholder):
        current_kwargs["label_length"] = label_length
    if not isinstance(logging_name, _DefaultPlaceholder):
        current_kwargs["logging_name"] = logging_name
    if not isinstance(max_identifier_length, _DefaultPlaceholder):
        current_kwargs["max_identifier_length"] = max_identifier_length
    if not isinstance(max_overflow, _DefaultPlaceholder):
        current_kwargs["max_overflow"] = max_overflow
    if not isinstance(module, _DefaultPlaceholder):
        current_kwargs["module"] = module
    if not isinstance(paramstyle, _DefaultPlaceholder):
        current_kwargs["paramstyle"] = paramstyle
    if not isinstance(pool, _DefaultPlaceholder):
        current_kwargs["pool"] = pool
    if not isinstance(poolclass, _DefaultPlaceholder):
        current_kwargs["poolclass"] = poolclass
    if not isinstance(pool_logging_name, _DefaultPlaceholder):
        current_kwargs["pool_logging_name"] = pool_logging_name
    if not isinstance(pool_pre_ping, _DefaultPlaceholder):
        current_kwargs["pool_pre_ping"] = pool_pre_ping
    if not isinstance(pool_size, _DefaultPlaceholder):
        current_kwargs["pool_size"] = pool_size
    if not isinstance(pool_recycle, _DefaultPlaceholder):
        current_kwargs["pool_recycle"] = pool_recycle
    if not isinstance(pool_reset_on_return, _DefaultPlaceholder):
        current_kwargs["pool_reset_on_return"] = pool_reset_on_return
    if not isinstance(pool_timeout, _DefaultPlaceholder):
        current_kwargs["pool_timeout"] = pool_timeout
    if not isinstance(pool_use_lifo, _DefaultPlaceholder):
        current_kwargs["pool_use_lifo"] = pool_use_lifo
    if not isinstance(plugins, _DefaultPlaceholder):
        current_kwargs["plugins"] = plugins
    if not isinstance(query_cache_size, _DefaultPlaceholder):
        current_kwargs["query_cache_size"] = query_cache_size
    current_kwargs.update(kwargs)
    return _create_engine(url, **current_kwargs)  # type: ignore
