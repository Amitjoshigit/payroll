
from fastapi import UploadFile,HTTPException
import pandas as pd
import io
import traceback


def validate_uploaded_excel(upload_file: UploadFile):
    try:
        content = upload_file.file.read()
        df = pd.read_excel(io.BytesIO(content), engine='openpyxl')

        # Define the required columns
        required_columns = ["fname", "mname", "lname", "emp_id", "designation", "department", "email_id", "phone_number", "date_of_joining"]

        # Check for missing columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            missing_columns_str = ', '.join(missing_columns)
            raise HTTPException(status_code=400, detail=f"Missing columns: {missing_columns_str}")

        # Check if each required column has data
        missing_data_columns = [col for col in required_columns if pd.isna(df[col]).any()]
        if missing_data_columns:
            missing_data_columns_str = ', '.join(missing_data_columns)
            raise HTTPException(status_code=400, detail=f"Columns with missing data: {missing_data_columns_str}")

        return df
    except HTTPException as e:
        raise e  # Re-raise FastAPI HTTPException with detailed information
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
