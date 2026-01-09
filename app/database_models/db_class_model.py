from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DBClassModel(Base):
    __tablename__ = 'classes'

    class_id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String(255), unique=True, index=True)