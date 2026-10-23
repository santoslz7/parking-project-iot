from functools import wraps
import hmac

from flask import request, jsonify

from config import Config


def require_device(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        enviado = request.headers.get("X-Device-Secret")
        esperado = Config.DEVICE_SHARED_SECRET

        if not esperado or not enviado or not hmac.compare_digest(
            enviado.encode("utf-8"), esperado.encode("utf-8")
        ):
            return jsonify({"error": "Não autorizado."}), 401

        return f(*args, **kwargs)
    return wrapper