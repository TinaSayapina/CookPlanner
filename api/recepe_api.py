from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import openai
from deep_translator import GoogleTranslator
from deepinfra.main import *
import hashlib

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


# Делаем строгую типизацию
class PromptRequest(BaseModel):
    prompt: str


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

