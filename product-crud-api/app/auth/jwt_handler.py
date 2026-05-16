from jose import jwt
from datetime import datetime, timedelta, timezone
from config.settings import settings
import uuid


SECRET_KEY = settings.SECRET_KEY
AlGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 3


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type":"access"})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=AlGORITHM)

def create_refresh_token(user_id: int):
    
    payload = {
        "sub": str(user_id),
        "jti": str(uuid.uuid4()),
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )
    }
    
    
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=AlGORITHM
    )