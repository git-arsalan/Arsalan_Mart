from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime
from pydantic import EmailStr
from typing import Union, Optional, Annotated

## defining base model class for user

class baseUser (SQLModel, table=True):
    user_key : int | None = Field(default=None, primary_key=True) 
    user_name: str
    login_id: str
    password: str
    phone: str = Field(max_digits=11)
    email: EmailStr
    created_on: datetime
    

class Auth_User (SQLModel):
    login_id: str
    password: str
