from pydantic import BaseModel
from fastapi import (APIRouter, Request,
                     Response, HTTPException,
                     Depends)
from jwt_auth.main import config, security
from database.userservice import *
from fastapi.responses import RedirectResponse
import re

# схема для логина
class UserLoginSchema(BaseModel):
    login: str
    password: str

# схема для регистрации
class RegistrationSchema(BaseModel):
    nickname: str
    phone_number: int
    password: str
    password2: str


# маршрут для юзеров
user_router = APIRouter(prefix="/user", tags=["Пользовательская часть"])

# Регистрация
@user_router.post("/register")
async def registration(info: RegistrationSchema, response: Response):
    # Проверка совпадения паролей
    if info.password != info.password2:
        return {"status": 0, "message": "Пароли не совпадают"}

    if len(info.password) < 5:
        return {"status":0, "message":"Пароль должен содержать не менее 5 символов"}

    # Проверка номера телефона по регулярному выражению
    phone_pattern = r"^\d{9}$"
    if not re.match(phone_pattern, str(info.phone_number)):
        return {"status": 0, "message": "Некорректный формат номера телефона"}


    result = registration_db(nickname=info.nickname, phone_number=info.phone_number,
                             password=info.password)
    print(result.get('status'))
    if result.get('status') == 1:
        token = security.create_access_token(uid='101')
        # сохраняем токен в куки пользователя
        response.set_cookie(key=config.JWT_ACCESS_COOKIE_NAME, value=token)
        return {
            "access_token": token,
            "status": 1
        }
    elif result.get('status') == 0:
        return {"status": 0, "message": result.get("message")}


# Логин
@user_router.post("/login")
async def login_with_jwt(credentials: UserLoginSchema, response: Response):
    result = login_db(credentials.login, credentials.password)

    if result:
        token = security.create_access_token(uid='101')
        # сохраняем токен в куки пользователя
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {
            "access_token": token,
            "status": 1
        }
    return {"status": 0, "message": "Неправильный пароль или логин"}


# функция с проверкой токена
@user_router.get("/test", dependencies=[Depends(security.access_token_required)])
async def test(request: Request):
    return "ok"


# функция для выхода из аккаунта
@user_router.get("/logout")
async def logout(response: Response, request: Request):
    response = RedirectResponse(url='/')
    response.delete_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        path='/',
    )
    return response
