from flask import Blueprint, jsonify, request

from firestore_client import get_db
from services.availability import InvalidPeriod, get_availability, parse_period

bp = Blueprint("parking_lots", __name__)

PUBLIC_FIELDS = ["name", "address", "latitude", "longitude", "hourly_rate", "opening_hours"]


def _public(doc):
    data = doc.to_dict()
    out = {"id": doc.id}
    out.update({k: data.get(k) for k in PUBLIC_FIELDS})
    return out


@bp.get("/api/parking-lots")
def list_parking_lots():
    db = get_db()
    docs = db.collection("parking_lots").where("active", "==", True).stream()
    return jsonify([_public(d) for d in docs]), 200


@bp.get("/api/parking-lots/<lot_id>/availability")
def availability(lot_id):
    db = get_db()
    lot = db.collection("parking_lots").document(lot_id).get()
    if not lot.exists or not lot.to_dict().get("active", False):
        return jsonify({"error": "Estacionamento não encontrado."}), 404

    try:
        arrival, departure = parse_period(
            request.args.get("arrival"), request.args.get("departure")
        )
    except InvalidPeriod as e:
        return jsonify({"error": str(e)}), 400

    result = get_availability(lot_id, arrival, departure)
    result.update({
        "parking_lot_id": lot_id,
        "arrival": arrival.isoformat(),
        "departure": departure.isoformat(),
    })
    return jsonify(result), 200
