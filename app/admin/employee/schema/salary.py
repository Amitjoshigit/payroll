from pydantic import BaseModel, EmailStr
from typing import Optional


class Earning(BaseModel):
    monthly_ctc: float
    basic: float
    da: float
    hra: float
    allowances: float
    other_special_allowances: float

class Deduction(BaseModel):
    epf: float
    esic: float
    pt: float
    gratuity: float
    medical_insurance: float
    others: float

class Salary(BaseModel):
    ctc_template: str
    annual_ctc: float
    earning: Earning
    deduction: Deduction
    gross_salary: float
    net_salary: float
    employee_id: str
