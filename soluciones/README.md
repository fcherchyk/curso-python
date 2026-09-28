# Soluciones de referencia

Mirá cada una **después** de que tus tests pasen.

Para correr los tests contra la solución de un día sin tocar tu código:

```bash
cp semana1/dia1_idiomatico/ejercicios.py /tmp/mio.py                       # backup
cp soluciones/semana1/dia1_idiomatico.py semana1/dia1_idiomatico/ejercicios.py
uv run pytest semana1/dia1_idiomatico
cp /tmp/mio.py semana1/dia1_idiomatico/ejercicios.py                       # restaurar
```
