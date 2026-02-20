import os
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv



# Load dotenv only locally
if os.getenv("RENDER") is None:
    load_dotenv()

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Password functions
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT functions
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    secret_key = os.getenv("SECRET_KEY")

    if not secret_key:
        raise RuntimeError("SECRET_KEY not found in environment")

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    print("SECRET_KEY VALUE:", secret_key)
    print("SECRET_KEY TYPE:", type(secret_key))

    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)