from exercise import make_averager, make_counter, make_limiter, multipliers


def test_make_counter_independent():
    a, b = make_counter(), make_counter(10)
    assert [a(), a(), a()] == [0, 1, 2]
    assert [b(), b()] == [10, 11]
    assert a() == 3


def test_counter_is_closure():
    c = make_counter()
    assert c.__closure__, "it must be a closure (an inner function)"


def test_multipliers():
    fs = multipliers(4)
    assert len(fs) == 4
    assert [f(10) for f in fs] == [0, 10, 20, 30]
    assert multipliers(0) == []


def test_make_averager():
    avg = make_averager()
    assert avg(10) == 10.0
    assert avg(20) == 15.0
    assert avg(60) == 30.0


def test_averagers_independent():
    avg1, avg2 = make_averager(), make_averager()
    avg1(100)
    assert avg2(1) == 1.0


def test_make_limiter():
    allowed = make_limiter(2)
    assert [allowed(), allowed(), allowed(), allowed()] == [True, True, False, False]
    assert make_limiter(0)() is False
