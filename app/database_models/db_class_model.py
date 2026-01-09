from sqlalchemy import Column, Integer, String
from database import Base


class DBClassModel(Base):
    __tablename__ = 'classes'

    class_id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String(255), unique=True, index=True)