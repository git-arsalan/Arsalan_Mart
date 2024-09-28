from sqlmodel import SQLModel, Field
from typing import Optional

class MartUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    hashed_password: str

class UserCreate(SQLModel):
    name: str
    email: str
    password: str  # This is the plain password; we will hash i
