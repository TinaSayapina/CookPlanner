from fastapi import APIRouter, HTTPException, status
from database.userservice import *
from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    username: str
    phone_number: int
    password: str
    password2: str

user_router = APIRouter(prefix="/user",
                        tags=["ПОЛЬЗОВАТЕЛЬСКАЯ ЧАСТЬ"])

@user_router.post("/register")

async def register(req: RegisterRequest):
    if req.password != req.password2:
        return {
            "status": 0,
            "message": "Пароли не совпадают"
        }

    result = add_user_db(req.username, req.phone_number, req.password)
    return result
