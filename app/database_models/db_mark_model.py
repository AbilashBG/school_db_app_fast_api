from sqlalchemy import CheckConstraint, Column,Integer,ForeignKey
from database import Base

class DBMarkModel(Base):
    __tablename__ = 'marks'

    s_id = Column(Integer,ForeignKey('students.s_id'),primary_key=True)
    subject_id = Column(Integer,ForeignKey('subjects.subject_id'),primary_key=True)
    marks = Column(Integer,nullable=False)

# marks should be greater than 0 and must not be greater than 100
    __table_args__=(
        CheckConstraint(marks >= 0),
        CheckConstraint(marks <= 100),
    )