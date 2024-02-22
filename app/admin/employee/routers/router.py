from fastapi import APIRouter

from app.admin.employee.services.excel_api import router as excel_api_router
from app.admin.employee.services.cards import router as cards_router
from app.admin.employee.services.employee_basic_detail import router as employee_basic_details_router
from app.admin.employee.services.export_employee_data import router as export_employee_data_router
from app.admin.employee.services.bank_details import router as bank_detail_router
from app.admin.employee.services.document_details import router as document_details_router
from app.admin.employee.services.additional_details import router as additional_details_router
from app.admin.employee.services.salary_api import router as salary_api_router


api_router = APIRouter()



# employee registration api routes 
api_router.include_router(employee_basic_details_router,
                          prefix='/basic-details',
                          tags=['employee basic details'])

api_router.include_router(excel_api_router,
                          prefix='',
                          tags=['download and upload Excel API'])

api_router.include_router(cards_router,
                          prefix='',
                          tags=['Cards-details ctc,monthly-ctc'])

api_router.include_router(bank_detail_router,
                          prefix='/bank-details',
                          tags=['Bank Details'])

api_router.include_router(export_employee_data_router,
                          prefix='/export',    
                          tags=['Export Employee Data'])

api_router.include_router(document_details_router,
                          prefix='/document-details',
                          tags=['Document Details'])


api_router.include_router(additional_details_router,
                          prefix='/additional-details',
                          tags=['Additional Details'])


api_router.include_router(salary_api_router,
                          prefix='/salary_details',
                          tags=['Salary Details'])

