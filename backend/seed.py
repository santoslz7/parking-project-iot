"""Cria dados fictícios no Firestore. Pode rodar mais de uma vez (IDs fixos, sobrescreve)."""
from firestore_client import get_db

LOTS = [
    {
        "id": "centro",
        "name": "Unidade Centro",
        "address": "Região central (endereço aproximado)",
        "latitude": -12.5400,
        "longitude": -38.2300,
        "hourly_rate": 8.00,
        "opening_hours": "06:00-22:00",
        "active": True,
        "spaces": 10,
    },
    {
        "id": "shopping",
        "name": "Unidade Shopping",
        "address": "Próximo ao shopping (endereço aproximado)",
        "latitude": -12.5500,
        "longitude": -38.2400,
        "hourly_rate": 10.00,
        "opening_hours": "08:00-23:00",
        "active": True,
        "spaces": 8,
    },
]


def main():
    db = get_db()
    batch = db.batch()
    for lot in LOTS:
        lot = dict(lot)
        lot_id = lot.pop("id")
        n_spaces = lot.pop("spaces")
        batch.set(db.collection("parking_lots").document(lot_id), lot)
        for i in range(1, n_spaces + 1):
            batch.set(
                db.collection("spaces").document(f"{lot_id}-A{i:02d}"),
                {
                    "parking_lot_id": lot_id,
                    "label": f"A-{i:02d}",
                    "active": True,
                    "occupancy_state": "FREE",
                },
            )
    batch.commit()
    print("Seed concluído: 2 estacionamentos e 18 vagas.")


if __name__ == "__main__":
    main()
