from pydantic import BaseModel

class TeacherModel(BaseModel):
    t_id: int
    name: str
    subject: str
    class_id: int
    salary: float