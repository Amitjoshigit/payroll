

from fastapi import APIRouter, File, UploadFile, HTTPException

from fastapi.responses import StreamingResponse
import openpyxl
import io
import traceback

import pandas as pd

from app.admin.DB_connection import db
from app.admin.employee.services.utility import excel_api_util

router = APIRouter()


collection = db["excel_files"]
    
@router.post('/download_template')
async def download_template():
    try:
        # Create an Excel template with the required columns
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        required_columns = ["first_name", "middle_name", "last_name", "employee_id", "designation", "department", "email_id", "phone_number", "date_of_joining"]
        for col_num, header in enumerate(required_columns, 1):
            sheet.cell(row=1, column=col_num, value=header)

        # Save the template to a BytesIO buffer
        excel_buffer = io.BytesIO()
        workbook.save(excel_buffer)

        # Return the Excel template as a streaming response
        return StreamingResponse(
            io.BytesIO(excel_buffer.getvalue()),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment;filename=employee_template.xlsx"}
        )
    except Exception as e:
        print(f"Error in /api/download_template: {str(e)}")
        raise


@router.post('/upload_and_process')
async def upload_data(
    file: UploadFile = File(...),
    # Add other form fields as needed
):
    try:
        df = excel_api_util.validate_uploaded_excel(file)
        
        df['date_of_joining'] = pd.to_datetime(df['date_of_joining']).dt.strftime('%Y-%m-%d')
        # Process the data and store it in a list of dictionaries
        uploaded_data = df.to_dict(orient='records')

        if not uploaded_data:
            raise HTTPException(status_code=400, detail="No valid data found in the specified columns")

        # Add additional fields with null values
        for data in uploaded_data:
            data.update({
                "gender": None,
                "blood_group": None,
                "type_of_employee": None,
                "CTC": None,
                "address_line1": None,
                "address_line2": None,
                "differently_abled": None,
                "personal_email": None,
                "work_email": None,
                "phone_number": None,
                "alternate_phone_number": None,
                "work_location": None,
            })

        # Store the data in MongoDB
            
        collection.insert_many(uploaded_data)

        return {"message": "File uploaded and processed successfully. Data stored in MongoDB"}
    except HTTPException as e:
        raise e  # Re-raise FastAPI HTTPException
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")