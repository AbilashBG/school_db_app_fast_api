from pydantic import BaseModel
from datetime import date

class StudentModel(BaseModel):
    s_id: int
    name: str
    class_id: int
    dob: date  # Date in date format
    gender: str  # 'Male', 'Female', 'Other'
    fees_has_paid: bool
    
