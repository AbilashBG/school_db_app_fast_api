from pydantic import BaseModel
from typing import List

# student response
class StudentResponse(BaseModel):
    # must declare same variable spelling which are used in DBStudentModel
    s_id:int
    name:str

    # It (Config) tells Pydantic: “You are allowed to read data from ORM objects, not just dicts.”
    class Config:
        from_attributes = True

# teacher response
class TeacherResponse(BaseModel):
    # must declare same variable spelling which are used in DBTeacherModel
    t_id:int
    name:str
    subject:str

    # It (Config) tells Pydantic: “You are allowed to read data from ORM objects, not just dicts.”
    class Config:
        from_attributes = True


class ClassDetailResponse(BaseModel):
    class_id:int
    class_name:str
    students:List[StudentResponse]
    teachers:List[TeacherResponse]

    # It (Config) tells Pydantic: “You are allowed to read data from ORM objects, not just dicts.”
    class Config:
        from_attributes = True