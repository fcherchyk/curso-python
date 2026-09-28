"""Código a testear (no lo modifiques: escribí los tests en ejercicio.py)."""


def es_bisiesto(anio: int) -> bool:
    """Bisiesto: divisible por 4, salvo los divisibles por 100 que no lo son por 400."""
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)


def dias_del_mes(anio: int, mes: int) -> int:
    """Cantidad de días del mes (1-12). Mes inválido → ValueError."""
    if not 1 <= mes <= 12:
        raise ValueError(f"mes inválido: {mes}")
    if mes == 2:
        return 29 if es_bisiesto(anio) else 28
    return 30 if mes in (4, 6, 9, 11) else 31
