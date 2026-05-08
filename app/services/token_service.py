import jwt
from datetime import datetime, timedelta, timezone
from app.config import SECRET_KEY, ALGORITHM
import sentry_sdk


def generate_token(user):
    payload = {
        "user_id": user.id,
        "role": user.role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token expired.")
        return None
    except jwt.InvalidTokenError as e:
        sentry_sdk.capture_exception(e)
        print("Invalid token.")
        return None
