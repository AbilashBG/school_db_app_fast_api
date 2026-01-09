from sqlalchemy import Column, Integer, String
from database import Base

class DBSubjectModel(Base):
    __tablename__ = "subjects"

    subject_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    subject_name = Column(String(50), nullable=False)
