import firebase_admin
from firebase_admin import credentials, firestore

from config import Config

_db = None


def get_db():
    """Cliente Firestore (singleton). Credenciais vêm de GOOGLE_APPLICATION_CREDENTIALS."""
    global _db
    if _db is None:
        if not firebase_admin._apps:
            firebase_admin.initialize_app(
                credentials.ApplicationDefault(),
                {"projectId": Config.FIREBASE_PROJECT_ID},
            )
        _db = firestore.client()
    return _db
