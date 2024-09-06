from datetime import datetime, timedelta
import jwt
import bcrypt

from core.config import settings

# private_key = b"-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBS..."
# public_key = b"-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEAC..."


def encode_jwt(payload: dict,
               private_key=settings.auth_jwt.private_key_path.read_text(),
               algorithm=settings.auth_jwt.algorithm,
               expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
               expire_timedelta: timedelta | None = None):
    encoded = jwt.encode(payload, key=private_key, algorithm=algorithm)
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now
    )
    encoded = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm
    )
    return encoded


def decode_jwt(token: str | bytes,
               public_key: str = settings.auth_jwt.public_key_path.read_text(),
               algorithm: str = settings.auth_jwt.algorithm):
    decoded = jwt.decode(token, key=public_key, algorithms=[algorithm])
    return decoded


def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(password=pwd_bytes, salt=salt)


def validate_password(password: str, hash_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(),
                          hashed_password=hash_password)
