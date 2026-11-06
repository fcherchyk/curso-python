from exercise import most_expensive, sort_by, sort_case_insensitive, sort_people


def test_sort_people():
    people = [
        {"name": "Zoe", "age": 30},
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30},
    ]
    assert sort_people(people) == ["Bob", "Zoe", "Alice"]


def test_sort_people_does_not_mutate():
    people = [{"name": "B", "age": 1}, {"name": "A", "age": 2}]
    sort_people(people)
    assert people[0]["name"] == "B"


def test_most_expensive():
    products = [
        {"name": "bread", "price": 1.2},
        {"name": "coffee", "price": 9.8},
        {"name": "tea", "price": 9.8},
    ]
    assert most_expensive(products) == "coffee"


def test_most_expensive_empty():
    assert most_expensive([]) is None


def test_sort_case_insensitive():
    assert sort_case_insensitive(["banana", "Apple", "Cherry", "apple"]) == [
        "Apple",
        "apple",
        "banana",
        "Cherry",
    ]


def test_sort_by_several_fields():
    rows = [
        {"country": "US", "city": "Seattle"},
        {"country": "CA", "city": "Toronto"},
        {"country": "CA", "city": "Calgary"},
    ]
    res = sort_by(rows, "country", "city")
    assert [r["city"] for r in res] == ["Calgary", "Toronto", "Seattle"]


def test_sort_by_without_fields():
    rows = [{"a": "2"}, {"a": "1"}]
    res = sort_by(rows)
    assert res == rows
    assert res is not rows
