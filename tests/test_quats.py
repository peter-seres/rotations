import foo


def test_hello():
    x = foo.hello("World")
    assert type(x) is str


def test_factorial():
    x = foo.factorial([1, 2, 3])
    assert (x == [1, 2, 6]).all()
