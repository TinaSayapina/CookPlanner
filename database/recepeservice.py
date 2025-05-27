from database import get_db
from database.models import *

# Добавляем новый рецепт в бд
def add_recepe_db(name, ingredients,recipe,pp_recipe):
    with next(get_db()) as db:
        # Проверка на уникальность названия
        recepe = db.query(Recipe).filter(Recipe.name == name).first()
        if recepe:
            return {
                "status": 0,
                "message": "Такой рецепт уже есть"
            }

        # Создаем новый рецепт в бд
        recepe = Recipe(name=name,ingredients=ingredients, recipe=recipe, pp_recipe=pp_recipe)
        db.add(recepe)
        db.commit()
        db.refresh(recepe)
        return {
            "status": 1,
            "message": recepe.id
        }

# Ищем рецепт в бд по названию
def get_recepe_db(name):
    with next(get_db()) as db:
        recepe = db.query(Recipe).filter(Recipe.name == name).first()
        return False if not recepe else recepe
