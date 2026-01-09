from pydantic import BaseModel

class SubjectModel(BaseModel):
    subject_id: int
    subject_name: str
