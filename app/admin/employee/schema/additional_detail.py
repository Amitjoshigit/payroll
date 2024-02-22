
from typing import Dict, Optional,List

from pydantic import BaseModel


class AdditionalDetailsAttributes(BaseModel):
    employee_id : str
    type_of_employee : str
    employee_benefit : List[str]
    employee_status : str
    type : Optional[str]  = None
    reason : Optional[str] = None

