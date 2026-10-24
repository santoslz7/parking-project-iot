import math
from decimal import Decimal, ROUND_HALF_UP


def calculate_price(hourly_rate, arrival, departure):
    """Calcula o preço da reserva. Sempre executado no servidor."""
    if departure <= arrival:
        raise ValueError("O horário de saída deve ser posterior ao horário de chegada.")

    taxa = Decimal(str(hourly_rate))
    if taxa < 0:
        raise ValueError("Tarifa inválida.")

    segundos = (departure - arrival).total_seconds()
    horas = max(1, math.ceil(segundos / 3600))

    return (taxa * horas).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)