import re
from urllib.parse import urlencode

# Swaps separators: US/English format -> Argentine format.
_TO_AR_FORMAT = str.maketrans({",": ".", ".": ","})


def format_pesos(amount: float) -> str:
    return "$ " + f"{amount:,.2f}".translate(_TO_AR_FORMAT)


def slug(title: str) -> str:
    return "-".join(re.findall(r"\w+", title.lower()))


def parse_options(text: str) -> dict[str, str]:
    options = {}
    for segment in text.split(";"):
        if not segment.strip():
            continue
        key, _, value = segment.partition("=")
        options[key.strip()] = value.strip()
    return options


def build_url(host: str, *segments: str, https: bool = True, **query: str | int) -> str:
    scheme = "https" if https else "http"
    url = f"{scheme}://{host}/" + "/".join(segments)
    if query:
        url += "?" + urlencode(query)
    return url
