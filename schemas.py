from typing import Optional
from pydantic import BaseModel

class UserRequestModel(BaseModel):
    username: str
    email: str

class UserResponseModel(UserRequestModel):
    id: int