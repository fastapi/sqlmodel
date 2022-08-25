from unittest.mock import patch

from sqlmodel import create_engine

from ...conftest import get_testing_print_function

expected_calls = [
    [
        "Created villain:",
        {
            "name": "Thinnus",
            "power_level": 9001,
            "id": 1,
            "boss_id": None,
        },
    ],
    [
        "Created villain:",
        {
            "name": "Ebonite Mew",
            "power_level": 400,
            "id": 3,
            "boss_id": 1,
        },
    ],
    [
        "Created villain:",
        {
            "name": "Dark Shorty",
            "power_level": 200,
            "id": 4,
            "boss_id": 1,
        },
    ],
    [
        "Created villain:",
        {
            "name": "Ultra Bot",
            "power_level": 2 ** 9,
            "id": 2,
            "boss_id": None,
        },
    ],
    [
        "Updated villain:",
        {
            "name": "Ultra Bot",
            "power_level": 2 ** 9,
            "id": 2,
            "boss_id": 1,
        },
    ],
    [
        "Added minion:",
        {
            "name": "Clone Bot 1",
            "power_level": 2 ** 6,
            "id": 5,
            "boss_id": 2,
        },
    ],
    [
        "Added minion:",
        {
            "name": "Clone Bot 2",
            "power_level": 2 ** 6,
            "id": 6,
            "boss_id": 2,
        },
    ],
    [
        "Added minion:",
        {
            "name": "Clone Bot 3",
            "power_level": 2 ** 6,
            "id": 7,
            "boss_id": 2,
        },
    ],
]


def test_tutorial(clear_sqlmodel):
    from docs_src.advanced.self_referential import tutorial001 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == expected_calls
