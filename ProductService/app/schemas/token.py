from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    first_name: str| None
    last_name: str| None = None
    email: str
    roles: list[str] = []
