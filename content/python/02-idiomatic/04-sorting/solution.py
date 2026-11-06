from operator import itemgetter


def sort_people(people: list[dict[str, str | int]]) -> list[str]:
    ordered = sorted(people, key=lambda p: (-int(p["age"]), str(p["name"])))
    return [str(p["name"]) for p in ordered]


def most_expensive(products: list[dict[str, str | float]]) -> str | None:
    if not products:
        return None
    # max returns the first one among the tied elements.
    return str(max(products, key=itemgetter("price"))["name"])


def sort_case_insensitive(words: list[str]) -> list[str]:
    return sorted(words, key=str.lower)


def sort_by(rows: list[dict[str, str]], *fields: str) -> list[dict[str, str]]:
    if not fields:
        return list(rows)
    return sorted(rows, key=itemgetter(*fields))
