from database import get_db
from database.models import *
recipes = [
    {
        "name": "Борщ",
        "ingredients": "свекла, капуста, картофель, морковь, лук, мясо",
        "recipe": "Обжарить овощи, варить с мясом, добавить свеклу и капусту.",
        "pp_recipe": "Можно добавить немного сметаны."
    },
    {
        "name": "Оливье",
        "ingredients": "Картофель, морковь, яйца, огурцы, колбаса, майонез",
        "recipe": "Отварить все овощи и яйца, нарезать и смешать с майонезом.",
        "pp_recipe": "Обеспечить низкую калорийность майонеза."
    },
    {
        "name": "Нежный куриный бульйон",
        "ingredients": "Курица, морковь, лук, сельдерей, специи",
        "recipe": "Варить курицу с овощами, процедить бульон.",
        "pp_recipe": "Добавить зелень для аромата."
    },
    {
        "name": "Пельмени",
        "ingredients": "Мука, мясной фарш, лук, специи",
        "recipe": "Замесить тесто, накрутить пельмени и сварить.",
        "pp_recipe": "Можно подать со сметаной."
    },
    {
        "name": "Блины",
        "ingredients": "Мука, молоко, яйца, масло",
        "recipe": "Приготовить тесто, жарить тонкие блинчики.",
        "pp_recipe": "Добавить начинку по желанию."
    },
    {
        "name": "Котлета по-киевски",
        "ingredients": "Куриное филе, масло, панировка",
        "recipe": "Начинить куриное филе маслом, панировать и жарить.",
        "pp_recipe": "Подавать с картофельным пюре."
    },
    {
        "name": "Салат «Мимоза»",
        "ingredients": "Рыба, картофель, морковь, яйца, майонез",
        "recipe": "Сложить слоями, посыпать тертым сыром.",
        "pp_recipe": "Можно заменить рыбу на курицу."
    },
    {
        "name": "Щи",
        "ingredients": "Капуста, картофель, морковь, лук, мясо",
        "recipe": "Варить овощи с мясом, подавать горячим.",
        "pp_recipe": "Добавить сметану по вкусу."
    },
    {
        "name": "Гречка с мясом",
        "ingredients": "Гречка, мясо, лук, специи",
        "recipe": "Обжарить мясо с луком, варить гречку и смешать.",
        "pp_recipe": "Подавать с овощами."
    },
    {
        "name": "Каша манная",
        "ingredients": "Манная крупа, молоко, масло, сахар",
        "recipe": "Варить крупу в молоке, добавить масло и сахар.",
        "pp_recipe": "Можно добавлять фрукты."
    }
]

# Команда для добавления сразу многих рецептов
def add_bulk_recepes():
    with next(get_db()) as db:
        try:
            for r in recipes:
                new_recipe = Recipe(**r)
                db.add(new_recipe)
            db.commit()
            return{
                "status":1,
                "message":"Рецепты успешно добавлены."
            }

        except Exception as e:
            db.rollback()  # откат изменений при ошибке

            return {
                "status": 0,
                "message": f"Ошибка при добавлении рецептов:{e}"
            }



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

# Получаем список рецептов из бд
def get_popular_recepes():
    with next(get_db()) as db:
        recepes = db.query(Recipe).all()
        return False if not recepes else recepes[:10]

