from http.client import HTTPException

from database import get_db
from database.models import *
from sqlalchemy import or_
from hash_argon2 import *

# Регистрация юзеров
def registration_db(nickname, phone_number, password):
    # Проверка на уникальность логина и телефона
    with next(get_db()) as db:
        text = ""
        user = db.query(User).filter(User.nickname == nickname).first()
        if user:
            text += "- юзернейм\n"
        user = db.query(User).filter(User.phone_number == phone_number).first()
        if user:
            text += "- номер\n"
        if text:
            # Если есть ошибки, возвращаем сообщение
            return {
                "status": 0,
                "message": "Проблема с полями:\n" + text
            }
        # Создаем пользователя если все поля уникальны
        user = User(nickname=nickname, phone_number=phone_number, password=hash_password(password))
        db.add(user)
        db.commit()
        db.refresh(user)
        return {
            "status": 1,
            "message": user.id
        }


# вход в аккаунт (по нику или номеру)
def login_db(login, password):
    with next(get_db()) as db:
        user = db.query(User).filter(or_(User.nickname == login
                                         , User.phone_number == login)).first()
        if user:
            if not check_pw(password, user.password):
                return False
            return user.id

        return False