from pydantic import BaseModel, EmailStr
from typing import Optional


class Employee(BaseModel):
    name: str
    age: int
    position: str
    dob: str
    gender: str
    date_of_joining: str
    blood_group: str
    designation: str
    employee_id: str
    Department: str
    type_of_employee: str
    CTC: float
    address_line1: str
    address_line2: str
    differently_abled: str
    personal_email: str
    work_email: str
    phone_number: str
    alternate_phone_number: str
    work_location: str