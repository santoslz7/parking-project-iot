from datetime import datetime, timedelta, timezone
from decimal import Decimal

from services.pricing import calculate_price

inicio = datetime(2026, 11, 10, 14, 0, tzinfo=timezone.utc)


def preco(minutos, taxa=8.0):
    return calculate_price(taxa, inicio, inicio + timedelta(minutes=minutos))


assert preco(1) == Decimal("8.00"), "1 minuto deve cobrar 1 hora"
assert preco(60) == Decimal("8.00"), "60 minutos deve cobrar 1 hora"
assert preco(61) == Decimal("16.00"), "61 minutos deve cobrar 2 horas"
assert preco(90) == Decimal("16.00"), "90 minutos deve cobrar 2 horas"
assert preco(120) == Decimal("16.00"), "2 horas deve cobrar 2 horas"
assert preco(60, taxa=7.5) == Decimal("7.50"), "tarifa com centavos"

for fim in (inicio, inicio - timedelta(minutes=30)):
    try:
        calculate_price(8.0, inicio, fim)
    except ValueError:
        pass
    else:
        raise AssertionError("saída igual ou antes da chegada deveria dar erro")

try:
    calculate_price(-1, inicio, inicio + timedelta(hours=1))
except ValueError:
    pass
else:
    raise AssertionError("tarifa negativa deveria dar erro")

print("Todos os testes de preço passaram.")