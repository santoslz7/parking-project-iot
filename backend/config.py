import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
    DEVICE_SHARED_SECRET = os.getenv("DEVICE_SHARED_SECRET")
    CORS_ORIGINS = [
        o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()
    ]
