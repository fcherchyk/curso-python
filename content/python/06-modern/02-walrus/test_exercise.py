import io

from exercise import extract_prices, first_ok, long_lengths, read_in_chunks


def test_read_in_chunks():
    assert read_in_chunks(io.StringIO("abcdefg"), 3) == ["abc", "def", "g"]
    assert read_in_chunks(io.StringIO(""), 3) == []


def test_long_lengths():
    assert long_lengths(["a", "hello", "world", "me"], 2) == [5, 5]


def test_extract_prices():
    assert extract_prices(["coffee $ 2.5", "no price", "bread $3", "$ 10.25 total"]) == [
        2.5,
        3.0,
        10.25,
    ]


def test_first_ok():
    responses = iter([None, None, "ok", "other"])
    calls = []

    def attempt():
        calls.append(1)
        return next(responses)

    assert first_ok(attempt, 5) == "ok"
    assert len(calls) == 3


def test_first_ok_exhausts():
    calls = []

    def fails():
        calls.append(1)
        return None

    assert first_ok(fails, 4) is None
    assert len(calls) == 4
