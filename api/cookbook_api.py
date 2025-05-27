from fastapi import APIRouter, HTTPException, status, Response
from pydantic import BaseModel
from typing import List, Optional
from database.cookbookservice import *

# Создаем маршрут для рецептов
cookbook_router = APIRouter(prefix="/cookbook", tags=["КНИГА РЕЦЕПТОВ"])


# Делаем строгую типизацию
class CookbookBase(BaseModel):
    user_id: int
    recepe_name:str
    notes: Optional[str] = None
    cooked: bool

# Добавление рецептов
@cookbook_router.post("/new")
async def addCookbook(info:CookbookBase, response: Response):
    result =add_cookbook_db(user_id=info.user_id, recepe_name=info.recepe_name)
    if result.get('status') == 1:
        return {"status": 1, "message": result.get("message")}
    elif result.get('status') == 0:
        return {"status": 0, "message": result.get("message")}