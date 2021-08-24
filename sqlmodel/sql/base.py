from typing import Generic, TypeVar

from sqlalchemy.sql.base import Executable as _Executable

_T = TypeVar("_T")


class Executable(_Executable, Generic[_T]):
    def __init__(self, *args, **kwargs):
        self.__dict__["_exec_options"] = kwargs.pop("_exec_options", None)
        super(_Executable, self).__init__(*args, **kwargs)
