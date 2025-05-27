from http.client import HTTPException

from database import get_db
from database.models import *

# Добавляем  рецепт в книгу рецептов
def add_cookbook_db(user_id, recepe_name):
    with next(get_db()) as db:
        try:
            cookbook = Cookbook(user_id=user_id,recepe_name=recepe_name)
            db.add(cookbook)
            db.commit()
            db.refresh(cookbook)
            return {
                "status": 1,
                "message": cookbook.id
            }
        except:
            raise HTTPException
