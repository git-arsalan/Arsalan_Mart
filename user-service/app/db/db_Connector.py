from app import settings
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import depends
from typing import Annotated


# only needed for psycopg 3 - replace postgresql
# with postgresql+psycopg in settings.DATABASE_URL
connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)
#connection_string = str(settings.DATABASE_URL)


# recycle connections after 5 minutes
# to correspond with the compute scale down
engine = create_engine(connection_string , connect_args={"sslmode": "require","pool_pre_ping":True}, pool_recycle=300, 
                       echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

db_Session = Annotated[Session, depends(get_session)]

