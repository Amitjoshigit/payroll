from typing import Optional
from pydantic import BaseModel





class Employee(BaseModel):
    first_name: str
    middle_name: Optional[str]
    last_name: str
    dob: str
    gender: str
    date_of_joining: str
    blood_group: str
    designation: str
    employee_id: str
    department: str
    type_of_employee: str
    ctc: Optional[float]
    address: str
    differently_abled: str
    personal_email: str
    work_email: str
    phone_number: str
    alternate_phone_number: str
    work_location: str

# Model for response including photo content
class EmployeeWithPhoto(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    date_of_joining: Optional[str] = None
    blood_group: Optional[str] = None
    designation: Optional[str] = None
    employee_id: Optional[str] = None 
    department: Optional[str] = None
    type_of_employee: Optional[str] = None
    ctc: Optional[float] = None
    address: Optional[str] = None
    differently_abled: Optional[str] = None
    personal_email: Optional[str] = None
    work_email: Optional[str] = None
    phone_number: Optional[str] = None
    alternate_phone_number: Optional[str]  = None
    work_location: Optional[str] = None
    photo_content: Optional[str] = None