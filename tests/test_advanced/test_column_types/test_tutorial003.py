from unittest.mock import patch

from sqlmodel import create_engine

from ...conftest import get_testing_print_function, needs_pydanticv2

expected_calls = [
    [
        "Avatar 1:",
        {
            "email": "tiangolo@example.com",
            "email_type": str,
            "ip_address": "127.0.0.1",
            "ip_address_type": str,
            "upload_location": "/uploads/1/123456789.jpg",
            "upload_location_type": str,
        },
    ],
]


@needs_pydanticv2
def test_tutorial(clear_sqlmodel):
    from docs_src.advanced.column_types import tutorial003 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == expected_calls
