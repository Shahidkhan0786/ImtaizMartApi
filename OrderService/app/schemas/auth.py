from pydantic import BaseModel

    
#  response from check token validity
class TokenResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    roles: list = []
    token_valid: bool 
    token_message: str

    

