from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import openai

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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Напиши ингредиенты для {request}"}],
            max_tokens=10
        )
        return {
            "status": 200,
            "message": response.choices[0].message.content
        }
    except Exception as error:
        return {
            "status": 0,
            "message": f"Ошибка {error}"
        }
