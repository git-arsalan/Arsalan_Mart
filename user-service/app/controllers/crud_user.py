from sqlmodel import Session,select
from app.models.user_models import MartUser,UserCreate
from typing import Optional
from passlib.context import CryptContext

def get_user_by_email(email: str, session: Session):
    statement = select(MartUser).where(MartUser.email == email)
    print(statement)
    user = session.exec(statement).first()
    print(user)
    return user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

""" async def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=user.password  # Normally you'd hash the password here
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user """
