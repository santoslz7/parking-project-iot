from datetime import datetime, timezone

from firestore_client import get_db

# Reservas que ocupam vaga no período
BLOCKING_STATUSES = ["PENDING_PAYMENT", "CONFIRMED", "CHECKED_IN"]


class InvalidPeriod(ValueError):
    pass


def parse_period(arrival_raw, departure_raw):
    """Converte strings ISO 8601 (com fuso, ex.: 2026-10-24T14:00:00-03:00) e valida o período."""
    if not arrival_raw or not departure_raw:
        raise InvalidPeriod("Informe 'arrival' e 'departure'.")
    try:
        arrival = datetime.fromisoformat(arrival_raw)
        departure = datetime.fromisoformat(departure_raw)
    except ValueError:
        raise InvalidPeriod("Datas devem estar no formato ISO 8601.")
    if arrival.tzinfo is None or departure.tzinfo is None:
        raise InvalidPeriod("Datas devem incluir fuso horário (ex.: -03:00 ou Z).")
    if departure <= arrival:
        raise InvalidPeriod("A saída deve ser posterior à chegada.")
    if arrival < datetime.now(timezone.utc):
        raise InvalidPeriod("A chegada não pode estar no passado.")
    return arrival, departure


def _is_blocking(res, arrival, departure, now):
    if res["status"] == "PENDING_PAYMENT":
        expires_at = res.get("expires_at")
        if expires_at is None or expires_at <= now:
            return False  # reserva pendente expirada não bloqueia
    return res["arrival_expected"] < departure and res["departure_expected"] > arrival


def get_availability(lot_id, arrival, departure):
    """Retorna vagas livres no período. Somente leitura; a reserva real usa transação."""
    db = get_db()
    now = datetime.now(timezone.utc)

    spaces = [
        s for s in db.collection("spaces")
        .where("parking_lot_id", "==", lot_id).stream()
        if s.to_dict().get("active", True)
    ]

    reservations = [
        r.to_dict() for r in db.collection("reservations")
        .where("parking_lot_id", "==", lot_id)
        .where("status", "in", BLOCKING_STATUSES).stream()
    ]
    busy_space_ids = {
        r.get("space_id") for r in reservations
        if _is_blocking(r, arrival, departure, now)
    }

    free = [s.id for s in spaces if s.id not in busy_space_ids]
    return {
        "total_spaces": len(spaces),
        "available_spaces": len(free),
        "available_space_ids": free,
    }
