

from fastapi import APIRouter, File, UploadFile, HTTPException

from fastapi.responses import StreamingResponse
import openpyxl
import io
import traceback

from ...DB_connection import db
from ..views import validation

router = APIRouter()


collection = db["excel_files"]
    
@router.post('/download_template')
async def download_template():
    try:
        # Create an Excel template with the required columns
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        required_columns = ["First_Name", "Middle_Name", "Last_Name", "emp_id", "designation", "department", "email_id", "phone_number", "date_of_joining"]
        for col_num, header in enumerate(required_columns, 1):
            sheet.cell(row=1, column=col_num, value=header)

        # Save the template to a BytesIO buffer
        excel_buffer = io.BytesIO()
        workbook.save(excel_buffer)

        # Return the Excel template as a streaming response
        return StreamingResponse(
            io.BytesIO(excel_buffer.getvalue()),
            media_type="routerlication/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment;filename=employee_template.xlsx"}
        )
    except Exception as e:
        print(f"Error in /api/download_template: {str(e)}")
        raise

@router.post('/upload_and_process')
async def upload_data(upload_file: UploadFile = File(...)):
    try:
        df = validation.validate_uploaded_excel(upload_file)

        # Process the data and store it in a list of dictionaries
        uploaded_data = df.to_dict(orient='records')

        if not uploaded_data:
            raise HTTPException(status_code=400, detail="No valid data found in the specified columns")

        # Store the data in MongoDB
        collection.insert_many(uploaded_data)

        return {"message": "File uploaded and processed successfully. Data stored in MongoDB"}
    except HTTPException as e:
        raise e  # Re-raise FastAPI HTTPException
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
