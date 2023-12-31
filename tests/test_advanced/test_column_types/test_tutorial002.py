from unittest.mock import patch

import pytest
from sqlmodel import create_engine

from ...conftest import get_testing_print_function, needs_pydanticv2

expected_calls = [
    ["Average score:", pytest.approx(0.5079, abs=0.0001)],
]


@needs_pydanticv2
def test_tutorial(clear_sqlmodel):
    from docs_src.advanced.column_types import tutorial002 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == expected_calls
