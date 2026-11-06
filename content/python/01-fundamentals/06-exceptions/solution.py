from pathlib import Path


def to_int(text: str, default: int | None = None) -> int | None:
    try:
        return int(text)  # int() already tolerates surrounding whitespace
    except ValueError:
        return default


class InsufficientFunds(Exception):
    def __init__(self, balance: float, amount: float) -> None:
        super().__init__(f"balance {balance} is not enough to withdraw {amount}")
        self.balance = balance
        self.amount = amount


def withdraw(balance: float, amount: float) -> float:
    if amount <= 0:
        raise ValueError(f"amount must be positive, got {amount!r}")
    if amount > balance:
        raise InsufficientFunds(balance, amount)
    return balance - amount


class ConfigError(Exception):
    pass


def read_config(path: Path) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        raise ConfigError(f"missing config file: {path}") from e
    config = {}
    for line in text.splitlines():
        if line.strip():
            key, _, value = line.partition("=")
            config[key.strip()] = value.strip()
    return config


def process_all(texts: list[str]) -> tuple[list[int], list[str]]:
    numbers: list[int] = []
    failed: list[str] = []
    for t in texts:
        try:
            n = int(t)
        except ValueError:
            failed.append(t)
        else:
            numbers.append(n)
    return numbers, failed
