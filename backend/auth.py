# auth.py
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

SECRET_KEY = "ton_secret_super_long"
pwd_context = CryptContext(schemes=["bcrypt"])

# Utilisateurs en dur (option simple du projet)
USERS = {"admin": pwd_context.hash("password123")}

def create_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str) -> str:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload["sub"]  # Retourne le username ou lève une exception
