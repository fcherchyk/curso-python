# pytest: fixtures, mocks and testable code

Testing pure functions is easy. The challenge shows up when the code **talks to the outside
world**: an API, a database, the disk or the clock. This chapter covers the three tools for
handling it: **fixtures** (setup and cleanup), **test doubles** (mocks and fakes) and, most
importantly, **designing code to be testable**.

## Fixtures: reusable setup

A fixture is a function that prepares something for the tests. Tests request it **by name**,
as a parameter, and pytest injects it:

```python
import pytest

@pytest.fixture
def users():
    return [{"id": 1, "name": "alice"}, {"id": 2, "name": "bob"}]

def test_count(users):                # pytest sees the parameter and calls the fixture
    assert len(users) == 2
```

Each test gets a **fresh** instance (with the default `function` scope), so tests don't
contaminate each other.

### Setup and teardown with `yield`

```python
@pytest.fixture
def connection():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE t (x)")
    yield conn                # what the test receives
    conn.close()              # cleanup: runs even if the test fails
```

### Scope and composition

```python
@pytest.fixture(scope="session")    # once for the whole run (expensive to create)
def db_engine(): ...

@pytest.fixture
def session(db_engine):             # fixtures can request other fixtures
    ...
```

Scopes: `function` (default), `class`, `module`, `package`, `session`.

### `conftest.py`

Fixtures defined in a `conftest.py` are available to every test in that folder and its
subfolders, **without importing them**. It's the place for shared fixtures.

### Built-in fixtures you'll use all the time

| Fixture       | What for                                                        |
|---------------|-----------------------------------------------------------------|
| `tmp_path`    | a unique temporary directory (`Path`) to read and write files   |
| `capsys`      | capture stdout/stderr: `capsys.readouterr().out`                |
| `monkeypatch` | replace attributes, environment variables or dicts during the test (and restore them) |
| `caplog`      | capture what gets logged                                        |

```python
def test_saves_file(tmp_path):
    path = tmp_path / "report.txt"
    save(path, data)
    assert path.read_text() == "..."

def test_reads_environment_variable(monkeypatch):
    monkeypatch.setenv("API_KEY", "test")
    assert read_config().api_key == "test"
```

## Designing for testability: dependency injection

Hard-to-test code usually looks like this:

```python
def temperature(city):
    r = httpx.get(f"https://api.weather.com/current?city={city}")   # hidden dependency
    return round(r.json()["temp_c"], 1)
```

To test it you have to intercept the network. Instead, if the dependency is **passed in**:

```python
class HttpClient(Protocol):
    def get_json(self, url: str) -> dict: ...

def temperature(city: str, client: HttpClient) -> float:
    data = client.get_json(f"{BASE}/current?city={city}")
    return round(data["temp_c"], 1)
```

the test hands it a **double** and that's it. The same goes for the clock
(`now: Callable[[], datetime]`), the id generator or the data repository. It's the basis of
how FastAPI handles dependencies (`Depends`), which you'll see later.

## Test doubles: fakes and mocks

**Fake**: a simple, real implementation, in memory.

```python
class FakeClient:
    def __init__(self, responses):
        self.responses = responses
        self.urls = []
    def get_json(self, url):
        self.urls.append(url)
        return self.responses[url]
```

**Mock**: an object that accepts any call and **records** how it was used. It ships with the
stdlib:

```python
from unittest.mock import Mock

client = Mock()
client.get_json.return_value = {"temp_c": 21.456}

assert temperature("Boston", client) == 21.5
client.get_json.assert_called_once_with(f"{BASE}/current?city=Boston")
```

The essentials of `Mock`:

```python
m.method.return_value = 42                      # what it returns
m.method.side_effect = KeyError("x")            # make it raise an exception
m.method.side_effect = [1, 2, KeyError()]       # a different response on each call
m.method.side_effect = lambda url: {...}        # compute the response
m.method.assert_called_once_with(...)           # verify the call
m.method.call_count, m.method.call_args_list
Mock(spec=HttpClient)                           # only accepts methods that exist in the spec
```

### `patch`: when you can't inject

If the dependency is "hardwired" inside the code, `unittest.mock.patch` (or
`monkeypatch.setattr`) replaces it **temporarily** in the module where it's **used**:

```python
from unittest.mock import patch

with patch("app.service.httpx.get") as get:
    get.return_value.json.return_value = {"temp_c": 20}
    ...
```

The rule is to patch where the name is looked up, not where it's defined. Use it as a last
resort: if you need lots of `patch` calls, that's usually a sign you should inject the
dependency.

## Don't overuse mocks

- Mock **at the edges** of the system (network, disk, clock, external services), not your
  own internal classes.
- If a test only checks that "X was called with Y" and no actual result, it's probably tied
  to the implementation and will break with every refactor.
- For a database, a **real** one in memory (SQLite) or in a container is often better than a
  mock.

## Summary

- Fixtures: setup via parameters, `yield` for cleanup, `scope` for reuse and `conftest.py`
  for sharing.
- `tmp_path`, `capsys` and `monkeypatch` handle files, console output and environment.
- Inject dependencies (typed with a Protocol) so you can pass doubles.
- `Mock` with `return_value`/`side_effect` and `assert_called_once_with`; `patch` as a last
  resort.
- Mock the edges, not your own code.

## Exercise

You write the tests for `weather.py` (the code is below). Requirements: a **fixture** of your
own, and using **`Mock`** and **`tmp_path`**. As in the previous chapter, your tests are run
against the original and against **4 mutants**.

```python
BASE = "https://api.weather.test/v1"

def temperature(city: str, client: HttpClient) -> float:
    data = client.get_json(f"{BASE}/current?city={city}")
    return round(data["temp_c"], 1)

def summary(cities: Iterable[str], client: HttpClient) -> dict[str, float]:
    """Temperature of each city. Those that fail with LookupError are skipped."""
    result = {}
    for city in cities:
        try:
            result[city] = temperature(city, client)
        except LookupError:
            continue
    return result

def save_report(path: Path, temperatures: dict[str, float]) -> None:
    """Writes "city: temp" per line, sorted by city."""
    lines = [f"{c}: {t}" for c, t in sorted(temperatures.items())]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
```

**Further reading:** [fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html),
[unittest.mock](https://docs.python.org/3/library/unittest.mock.html),
[monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html).
