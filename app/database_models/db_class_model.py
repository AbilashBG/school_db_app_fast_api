from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship


class DBClassModel(Base):
    __tablename__ = 'classes'

    class_id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String(255), unique=True, index=True)

    students = relationship(
        "DBStudentModel",
        cascade="all, delete",
        passive_deletes=True
    )

    teachers = relationship(
        "DBTeacherModel",
        cascade="all, delete",
        passive_deletes=True
    )