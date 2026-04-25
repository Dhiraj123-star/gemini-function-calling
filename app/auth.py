import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

# Load env
load_dotenv()

# -----------------------------
# CONFIG
# -----------------------------
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Use PBKDF2
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

# -----------------------
# In-memory user store
# {"username": "hashed password"}
# -----------------------

fake_users_db : dict[str,str]={}

# -----------------------------
# PASSWORD FUNCTIONS
# -----------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# -------------
# Signup
# -------------
def create_user(username: str, password:str)-> bool:
    """Returns False if username already taken."""
    if username in fake_users_db:
        return False
    fake_users_db[username]=  hash_password(password)
    return True


# -----------------------------
# AUTHENTICATION
# -----------------------------
def authenticate_user(username: str, password: str):
    hashed = fake_users_db.get(username)
    if not hashed or not verify_password(password,hashed):
        return None

    return {"username": username}


# -----------------------------
# TOKEN CREATION
# -----------------------------
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# -----------------------------
# TOKEN VERIFICATION
# -----------------------------
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None