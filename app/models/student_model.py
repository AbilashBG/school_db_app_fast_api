from pydantic import BaseModel
from datetime import date
from enum import Enum

class GenderEnum(str, Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"

class StudentModel(BaseModel):
    s_id: int
    name: str
    class_id: int
    dob: date  # Date in date format
    gender: GenderEnum  # 'Male', 'Female', 'Other'
    fees_has_paid: bool
    
