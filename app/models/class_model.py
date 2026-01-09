from pydantic import BaseModel

class ClassModel(BaseModel):
    class_id:int
    class_name:str
