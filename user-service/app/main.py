from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session
from app.models.user_models import MartUser,UserCreate
from app.controllers.crud_user import get_user_by_email,hash_password
from app.db.db_Connector import get_session, create_db_and_tables, DB_SESSION
#from kafka import KafkaProducer
from contextlib import asynccontextmanager
import json


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="User Service",
    description="API for managing users",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Users", "description": "Operations with users."}
    ]
)

#app = FastAPI()

# Initialize Kafka producer
""" producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
) """


################## Main Route #################################################
@app.get("/")
def home_route():
    return "This is user service"

##################     Register User Route ####################################

@app.post("/CreateUsers/") #Annotated[User, Depends(get_user_by_id_func)]
def add_user(user_data: UserCreate, session: Session = Depends(get_session)):
    try:
        # Check if the user already exists
        existing_user = get_user_by_email(user_data.email, session)
        print(user_data.email)
        
        if existing_user:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists."
            )
        
        # Hash the user's password
        hashed_password = hash_password(user_data.password)
        
        # Create a new User object
        new_user = MartUser(name=user_data.name, email=user_data.email, hashed_password=hashed_password)
        
        # Add and commit the new user to the database
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        print("new user:" + new_user)
        return f"user created successfully with name ={new_user.name}"
    except Exception as e:
        print("An error occurred:", e)
# if __name__ == "__main__":
#     import uvicorn
#     init_db()  # Initialize the database tables
#     uvicorn.run(app, host="0.0.0.0", port=8000)
