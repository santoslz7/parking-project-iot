from flask import Blueprint, jsonify, request

from auth import require_device

bp = Blueprint("iot", __name__)

TIPOS_VALIDOS = ("ENTRY", "EXIT")


@bp.post("/api/iot/access-request")
@require_device
def access_request():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({"error": "Corpo JSON inválido."}), 400

    event_id = dados.get("event_id")
    device_id = dados.get("device_id")
    tipo = dados.get("type")

    if not event_id or not device_id or tipo not in TIPOS_VALIDOS:
        return jsonify({"error": "Campos obrigatórios ausentes ou inválidos."}), 400

    # Por enquanto, nega sempre. A validação real da reserva vem depois.
    return jsonify({"authorized": False, "reason": "Acesso não autorizado."}), 200