from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

class DBTeacherModel(Base):
    __tablename__ = "teachers"

    t_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    subject = Column(String(50), nullable=False)

    # Foreign key relationship to classes table and class_id column
    class_id = Column(Integer, ForeignKey("classes.class_id"))
    salary = Column(Float(10,2),nullable=False)