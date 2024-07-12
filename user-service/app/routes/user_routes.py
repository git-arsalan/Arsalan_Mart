from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def get_users():
    pass # implementing later

@router.post("/addUsers")
def insert_users():
    pass # implementing later

@router.put("/editUser")
def insert_users():
    pass # implementing later

@router.patch("/updateUserStatus")
def insert_users():
    pass # implementing later

