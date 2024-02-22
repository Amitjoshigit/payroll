
from pydantic import BaseModel
from typing import List, Optional

# deleted employee id in bankdetail model
class BankDetail(BaseModel):
    bank_name: str
    ifsc_code: str
    account_number: str
    branch_code: str
    default_for_payroll: bool

class EmployeeBankDetails(BaseModel):
    employee_id: str
    bank_details: List[BankDetail]