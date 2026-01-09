from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, Boolean
from database import Base

class DBStudentModel(Base):
    __tablename__ = 'students'

    s_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    
    # Foreign key relationship to classes table and class_id column
    class_id = Column(Integer, ForeignKey('classes.class_id'))
    dob = Column(Date)
    gender = Column(String(10), nullable=False)
    fees_has_paid = Column(Boolean, default=False)  