from sqlalchemy import (Column, String, Integer,
                        DateTime, ForeignKey)
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


# модель юзеров
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    password = Column(String, nullable=True)
    reg_date = Column(DateTime, default=lambda: datetime.now())
