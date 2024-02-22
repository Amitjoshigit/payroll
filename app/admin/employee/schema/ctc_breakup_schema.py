
from pydantic import BaseModel

class EmployeeInput(BaseModel):
    employee_id: str
    ctc_template: str
    annual_ctc: float
