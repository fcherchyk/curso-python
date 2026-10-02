from pathlib import Path


def a_entero(texto: str, default: int | None = None) -> int | None:
    try:
        return int(texto)  # int() ya tolera espacios alrededor
    except ValueError:
        return default


class SaldoInsuficiente(Exception):
    def __init__(self, saldo: float, monto: float) -> None:
        super().__init__(f"saldo {saldo} insuficiente para retirar {monto}")
        self.saldo = saldo
        self.monto = monto


def retirar(saldo: float, monto: float) -> float:
    if monto <= 0:
        raise ValueError(f"el monto tiene que ser positivo, llegó {monto!r}")
    if monto > saldo:
        raise SaldoInsuficiente(saldo, monto)
    return saldo - monto


class ConfigError(Exception):
    pass


def leer_config(ruta: Path) -> dict[str, str]:
    try:
        texto = ruta.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        raise ConfigError(f"falta el archivo de configuración: {ruta}") from e
    config = {}
    for linea in texto.splitlines():
        if linea.strip():
            clave, _, valor = linea.partition("=")
            config[clave.strip()] = valor.strip()
    return config


def procesar_todos(textos: list[str]) -> tuple[list[int], list[str]]:
    numeros: list[int] = []
    fallidos: list[str] = []
    for t in textos:
        try:
            n = int(t)
        except ValueError:
            fallidos.append(t)
        else:
            numeros.append(n)
    return numeros, fallidos
