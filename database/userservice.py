from http.client import HTTPException

from database import get_db
from database.models import *

# Регистрация юзеров
def add_user_db(username, phone_number, password):

    with next(get_db()) as db:
        # Проверка на уникальность логина и телефона
        user = db.query(User).filter(User.username == username or User.phone_number == phone_number).first()
        if user:
            return {
                "status":0,
                "message":"Такой логин или телефон уже занят"
            }

        # Внесение нового пользователя в БД

        user = User(username=username, phone_number=phone_number, password=password)

        if not user:
            return{
                "status": 0,
                "message": "Не добавилось",
            }

        db.add(user)
        db.commit()
        db.refresh(user)
        return {
            "status": 1,
            "message": "Успешно добавлен",
        }
