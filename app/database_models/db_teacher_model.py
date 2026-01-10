from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class DBTeacherModel(Base):
    __tablename__ = 'teachers'

    t_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    subject = Column(String(50), nullable=False)

    # Foreign key relationship to classes table and class_id column
    class_id = Column(Integer, ForeignKey('classes.class_id',ondelete="CASCADE"), nullable=False)
    salary = Column(Integer, nullable=False)

    # back_populates connects both sides =>class & teachers
    class_obj = relationship("DBClassModel", back_populates="teachers")