from pydantic import BaseModel

class MarkModel(BaseModel):
    s_id:int
    subject_id:int
    marks:int