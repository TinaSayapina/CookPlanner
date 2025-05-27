from database import get_db
from database.models import *

def add_recepe_db(name, ingredients,recipe,pp_recipe):
    # Проверка на уникальность логина и телефона
    with next(get_db()) as db:
        text = ""
        recepe = db.query(Recipe).filter(Recipe.name == name).first()
        if recepe:
            return {
                "status": 0,
                "message": "Такой рецепт уже есть:\n" + text
            }
        # Создаем пользователя если все поля уникальны
        recepe = Recipe(name=name,ingredients=ingredients, recipe=recipe, pp_recipe=pp_recipe)
        db.add(recepe)
        db.commit()
        db.refresh(recepe)
        return {
            "status": 1,
            "message": recepe.id
        }
