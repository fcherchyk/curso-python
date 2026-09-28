import re
from urllib.parse import urlencode

# Intercambia separadores: formato inglés -> argentino.
_A_FORMATO_AR = str.maketrans({",": ".", ".": ","})


def formatear_pesos(monto: float) -> str:
    return "$ " + f"{monto:,.2f}".translate(_A_FORMATO_AR)


def slug(titulo: str) -> str:
    return "-".join(re.findall(r"\w+", titulo.lower()))


def parsear_opciones(texto: str) -> dict[str, str]:
    opciones = {}
    for segmento in texto.split(";"):
        if not segmento.strip():
            continue
        clave, _, valor = segmento.partition("=")
        opciones[clave.strip()] = valor.strip()
    return opciones


def construir_url(host: str, *segmentos: str, https: bool = True, **query: str | int) -> str:
    esquema = "https" if https else "http"
    url = f"{esquema}://{host}/" + "/".join(segmentos)
    if query:
        url += "?" + urlencode(query)
    return url
