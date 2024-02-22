from fastapi import Query,APIRouter
from fastapi.responses import StreamingResponse
import pandas as pd
from io import BytesIO
from fastapi.responses import StreamingResponse



from app.admin.DB_connection import employee_additional_details,employee_basic_collection,employee_banks_collection,employee_salaries_collection
from app.admin.employee.services.utility.export_data_util import export_data,get_salary_data,get_bank_data,CustomJSONEncoder

router = APIRouter()






json_encoder = CustomJSONEncoder()


@router.get("/basic-details/", response_class=StreamingResponse)
async def export_basic_details(format: str = Query("csv", description="Export format (csv, xlsx, pdf)")):
    employees = employee_basic_collection.find()
    employees_data = await employees.to_list(length=None)
    df = pd.json_normalize(employees_data)
    exported_data, content_type = export_data(df, format)

    # Add Content-Disposition header for download
    file_extension = format if format != "excel" else "xlsx"
    file_name = f"exported_basic_details.{file_extension}"
    headers = {
        "Content-Disposition": f"attachment; filename={file_name}"
    }
    

    return StreamingResponse(BytesIO(exported_data), media_type=content_type, headers=headers)



# Export additional details
@router.get("/additional-details", response_class=StreamingResponse)
async def export_additional_details(format: str = Query("csv", description="Export format (csv, xlsx, pdf)")):
    details_cursor = employee_additional_details.find()
    details_list = await details_cursor.to_list(length=None)
    df = pd.json_normalize(details_list)
    exported_data, content_type = export_data(df, format)

    # Add Content-Disposition header for download
    file_extension = format if format != "excel" else "xlsx"
    file_name = f"exported_additional_details.{file_extension}"
    headers = {
        "Content-Disposition": f"attachment; filename={file_name}"
    }

    return StreamingResponse(BytesIO(exported_data), media_type=content_type, headers=headers)


# Export salary details
@router.get("/salary-details", response_class=StreamingResponse)
async def export_salary_details(format: str = Query("csv", description="Export format (csv, xlsx, pdf)")):
    salary_details = await employee_salaries_collection.find().to_list(length=None)
    df = pd.json_normalize([get_salary_data(salary) for salary in salary_details])
    exported_data, content_type = export_data(df, format)

    # Add Content-Disposition header for download
    file_extension = format if format != "excel" else "xlsx"
    file_name = f"exported_salary_details.{file_extension}"
    headers = {
        "Content-Disposition": f"attachment; filename={file_name}"
    }

    return StreamingResponse(BytesIO(exported_data), media_type=content_type, headers=headers)

# Export bank details
@router.get("/bank-details", response_class=StreamingResponse)
async def export_bank_details(format: str = Query("csv", description="Export format (csv, xlsx, pdf)")):
    bank_details = await employee_banks_collection.find().to_list(length=None)
    df = pd.json_normalize([get_bank_data(bank) for bank in bank_details])
    exported_data, content_type = export_data(df, format)

    # Add Content-Disposition header for download
    file_extension = format if format != "excel" else "xlsx"
    file_name = f"exported_bank_details.{file_extension}"
    headers = {
        "Content-Disposition": f"attachment; filename={file_name}"
    }

    return StreamingResponse(BytesIO(exported_data), media_type=content_type, headers=headers)