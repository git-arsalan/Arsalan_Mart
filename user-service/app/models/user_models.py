from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr

class MartUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)
    hashed_password: str

class UserCreate(SQLModel):
    name: str
    email: EmailStr
    password: str  # This is the plain password; we will hash it later
