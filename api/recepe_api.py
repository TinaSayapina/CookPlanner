from fastapi import APIRouter, HTTPException, status, Response
from pydantic import BaseModel
import openai
from deep_translator import GoogleTranslator

from database.recepeservice import *
from deepinfra.main import *
import hashlib
from fastapi.responses import JSONResponse
from typing import List, Optional


# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values

# loading variables from .env file
load_dotenv()

# Создаем маршрут для рецептов
recepe_router = APIRouter(prefix="/recepe", tags=["РЕЦЕПТЫ И ИНГРЕДИЕНТЫ"])

# Достаем апи ключ openai из файла .env
openai.api_key = os.getenv("API_KEY")

cache = {}


# Делаем строгую типизацию для промпта
class PromptRequest(BaseModel):
    prompt: str

# Делаем строгую типизацию для рецепта
class RecipeBase(BaseModel):
    name: str
    ingredients: str
    recipe: str
    pp_recipe: Optional[str] = None

@recepe_router.post("/recepe")
async def chat_gpt(request: PromptRequest):
    # делаем первую букву заглавной
    prompt = request.prompt.capitalize()

    # Проверка на корректный промпт
    if not prompt.isalpha():
        return {
            "status": 0,
            "message": "Введите правильное название блюда"
        }
    print(get_recepe_db(prompt))
    # проверяем есть ли рецепт в бд
    recepe_from_bd=get_recepe_db(prompt)

    if recepe_from_bd:
        ingredients = recepe_from_bd.ingredients
        return{
            "status": 200,
            "message":ingredients
        }

    # если нет в бд то обращаемся в chat gpt
    else:
        try:
            # Создаем хэш ключа по входному запросу
            key = hashlib.sha256(prompt.encode()).hexdigest()
            # Проверяем наличие в кеше
            if key in cache:
                print("Кеш найден: ", cache[key])
                return {
                    "status": 200,
                    "message": cache[key]
                }

            # API запрос в chatGpt
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user",
                           "content": f"Напиши только список ингредиентов для {prompt} через запятую, без дополнительных слов."}],
                max_tokens=50
            )

            # Переводим промпт на английский при помощи сервиса Google translator
            # Временно отключила
            # prompt_en = GoogleTranslator(source='auto', target='en').translate(prompt)
            # Генерируем картинку по промпту с помощью api сервиса deepinfra
            # Временно отключила из-за того что закончилась подписка
            # generate_image(prompt=prompt_en)

            # Сохраняем в кеш
            result = response.choices[0].message.content
            cache[key] = result
            print("Обновленный кеш:", cache)  # Выводит все содержимое кеша

            return {
                "status": 200,
                "message": result
            }
        except Exception as error:
            return {
                "status": 0,
                "message": f"Ошибка {error}"
            }



# Добавление рецептов через админку
@recepe_router.post("/new")
async def addRecepe(info:RecipeBase, response: Response):
    result =add_recepe_db(name=info.name, ingredients=info.ingredients, recipe=info.recipe, pp_recipe=info.pp_recipe)
    if result.get('status') == 1:
        return {"status": 1, "message": result.get("message")}
    elif result.get('status') == 0:
        return {"status": 0, "message": result.get("message")}

@recepe_router.get("/popular")
async def getPopular():
    top10 = get_popular_recepes()
    if not top10:
        return {"status": 404, "message": "Нет популярных рецептов"}
    serialized = [serialize_recipe(r) for r in top10]
    return {"status": 200, "data": serialized}

def serialize_recipe(recipe):
    return {
        "id": recipe.id,
        "name": recipe.name,
        "ingredients": recipe.ingredients,
        "recipe": recipe.recipe,
        "pp_recipe": recipe.pp_recipe
    }
