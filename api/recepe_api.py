from fastapi import APIRouter, HTTPException, status, Response
from pydantic import BaseModel
import openai
from deep_translator import GoogleTranslator

from database.recepeservice import add_recepe_db
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
    # Проверка на корректный промпт
    if not request.prompt.isalpha():
        return {
            "status": 0,
            "message": "Введите правильное название блюда"
        }
    try:

        # Создаем хэш ключа по входному запросу
        key = hashlib.sha256(request.prompt.encode()).hexdigest()
        # Проверяем наличие в кеше
        if key in cache:
            print("Кеш найден: ", cache[key])
            return {
                "status": 200,
                "message": cache[key]
            }

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user",
                       "content": f"Напиши только список ингредиентов для {request.prompt} через запятую, без дополнительных слов."}],
            max_tokens=50
        )

        # Переводим промпт на английский при помощи сервиса Google translator
        prompt_en = GoogleTranslator(source='auto', target='en').translate(request.prompt)
        # Генерируем картинку по промпту с помощью api сервиса deepinfra
        generate_image(prompt=prompt_en)

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



# Admin
@recepe_router.post("/new")
async def addRecepe(info:RecipeBase, response: Response):

    result =add_recepe_db(name=info.name, ingredients=info.ingredients, recipe=info.recipe, pp_recipe=info.pp_recipe)
    print(result.get('status'))
    if result.get('status') == 1:
        ...
    elif result.get('status') == 0:
        return {"status": 0, "message": result.get("message")}