from sqlalchemy import (Column, String, Integer,
                        DateTime, ForeignKey, Boolean)
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# модель юзеров
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String, unique=True)
    phone_number = Column(Integer, unique=True)
    password = Column(String)
    reg_date = Column(DateTime, default=lambda: datetime.now())

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    ingredients = Column(String, nullable=False)
    recipe = Column(String, nullable=False)
    pp_recipe = Column(String, nullable=True)

    cookbooks = relationship("Cookbook", back_populates="recipe")

class Cookbook(Base):
    __tablename__ = "cookbooks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # или ForeignKey("users.id")
    recepe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    notes = Column(String, nullable=True)
    cooked = Column(Boolean, default=False)

    recipe = relationship("Recipe")