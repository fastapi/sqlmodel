from sqlmodel.default import Default


def test_default_bool() -> None:
    dt1 = Default(True)
    dt2 = Default(1)
    dt3 = Default("foo")
    dt4 = Default(["foo"])
    df1 = Default(False)
    df2 = Default(0)
    df3 = Default("")
    df4: list = Default([])
    df5 = Default(None)

    assert not not dt1
    assert not not dt2
    assert not not dt3
    assert not not dt4
    assert not df1
    assert not df2
    assert not df3
    assert not df4
    assert not df5


def test_equality() -> None:
    value1 = Default("foo")
    value2 = Default("foo")

    assert value1 == value2


def test_not_equality() -> None:
    value1 = Default("foo")
    value2 = Default("bar")

    assert not (value1 == value2)


def test_not_equality_other() -> None:
    value1 = Default("foo")
    value2 = "foo"

    assert not (value1 == value2)
