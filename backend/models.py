from sqlalchemy import Column, Integer, String
from db import Base

class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)