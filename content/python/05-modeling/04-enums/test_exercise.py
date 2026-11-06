import json

import pytest
from exercise import Estado, Permiso, Prioridad, mas_urgentes, puede


def test_estado_es_string():
    assert Estado.PENDIENTE == "pendiente"
    assert Estado("en_curso") is Estado.EN_CURSO
    assert json.dumps({"e": Estado.TERMINADO}) == '{"e": "terminado"}'


def test_estado_siguiente():
    assert Estado.PENDIENTE.siguiente() is Estado.EN_CURSO
    assert Estado.EN_CURSO.siguiente() is Estado.TERMINADO
    with pytest.raises(ValueError):
        Estado.TERMINADO.siguiente()


def test_estado_es_final():
    assert Estado.TERMINADO.es_final
    assert not Estado.PENDIENTE.es_final


def test_prioridad_ordenable():
    assert Prioridad.ALTA > Prioridad.BAJA
    assert Prioridad.MEDIA == 2


def test_mas_urgentes():
    tareas = [
        ("a", Prioridad.BAJA),
        ("b", Prioridad.ALTA),
        ("c", Prioridad.MEDIA),
        ("d", Prioridad.ALTA),
    ]
    assert mas_urgentes(tareas) == ["b", "d", "c", "a"]


def test_permisos():
    rw = Permiso.LEER | Permiso.ESCRIBIR
    assert puede(rw, Permiso.LEER)
    assert puede(rw, Permiso.LEER | Permiso.ESCRIBIR)
    assert not puede(rw, Permiso.BORRAR)
    assert not puede(rw, Permiso.TODOS)
    assert puede(Permiso.TODOS, Permiso.BORRAR)
