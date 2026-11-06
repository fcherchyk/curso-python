import itertools
import types

from exercise import bytes_by_status, first_even_squares, in_batches, parse_access_log

LOG = [
    "10.0.0.1 GET /index 200 512",
    "10.0.0.2 POST /api 500 128",
    "broken line",
    "10.0.0.1 GET /img 200 2048",
    "10.0.0.3 GET /x 404 abc",
    "10.0.0.4 GET /y 404 64",
]


def test_first_even_squares_with_infinite():
    assert first_even_squares(itertools.count(1), 4) == [4, 16, 36, 64]


def test_in_batches_with_list():
    assert list(in_batches([0, 1, 2, 3, 4, 5, 6], 3)) == [(0, 1, 2), (3, 4, 5), (6,)]
    assert list(in_batches([], 3)) == []


def test_in_batches_is_lazy():
    batches = in_batches(itertools.count(), 2)
    assert next(batches) == (0, 1)
    assert next(batches) == (2, 3)


def test_parse_access_log():
    res = parse_access_log(LOG)
    assert isinstance(res, types.GeneratorType)
    assert list(res) == [
        ("10.0.0.1", 200, 512),
        ("10.0.0.2", 500, 128),
        ("10.0.0.1", 200, 2048),
        ("10.0.0.4", 404, 64),
    ]


def test_bytes_by_status():
    assert bytes_by_status(LOG) == {200: 2560, 404: 64, 500: 128}
    assert list(bytes_by_status(LOG)) == [200, 404, 500]


def test_bytes_by_status_with_generator():
    assert bytes_by_status(line for line in LOG) == {200: 2560, 404: 64, 500: 128}
