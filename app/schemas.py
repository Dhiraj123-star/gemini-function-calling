from pydantic import BaseModel,field_validator

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str


class LoginRequest(BaseModel):
    username: str
    password: str


class SignupRequest(BaseModel):
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def password_strength(cls,v):
        if len(v)<6:
            raise ValueError("Password must be at least 6 characters")
        return v
    


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"