from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas import QueryRequest, QueryResponse, LoginRequest, TokenResponse,SignupRequest
from app.agent import run_agent
from app.auth import authenticate_user, create_access_token, verify_token,create_user

app = FastAPI()

security = HTTPBearer()


# -----------------------------
# AUTH DEPENDENCY
# -----------------------------
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload

# -----------
# SIGNUP
# -----------

@app.post("/signup",response_model=TokenResponse)
def signup(data: SignupRequest):
    success = create_user(data.username,data.password)
    if not success:
        raise HTTPException(status_code=400,detail="Username already taken ")

    # Auto login after signup
    token = create_access_token({"sub":data.username})
    return {"access_token":token}


# -----------------------------
# LOGIN ENDPOINT
# -----------------------------
@app.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    user = authenticate_user(data.username, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["username"]})
    return {"access_token": token}


# -----------------------------
# PROTECTED AI ENDPOINT
# -----------------------------
@app.post("/ask", response_model=QueryResponse)
def ask(data: QueryRequest, user=Depends(get_current_user)):
    result = run_agent(data.query)
    return {"response": result}