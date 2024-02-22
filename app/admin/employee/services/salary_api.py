from fastapi import HTTPException, APIRouter
from app.admin.employee.services.utility.ctc_breakup_util import calculate_ctc
from app.admin.employee.schema.ctc_breakup_schema import EmployeeInput
from app.admin.DB_connection import employee_salaries_collection

router = APIRouter()


@router.post("/generate_ctc" , description="Generate CTC and save it to MongoDB")
async def post_ctc(employee: EmployeeInput):
    try:
        result = calculate_ctc(employee)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{employee_id}")
async def get_ctc(employee_id: str):
    try:
        # Fetch data from MongoDB based on the provided 'employee_id'
        data = await employee_salaries_collection.find_one({"employee_id": employee_id})

        if not data:
            raise HTTPException(status_code=404, detail=f"Data for Employee with ID {employee_id} not found")
        
        # Convert the ObjectId to a string
        data["_id"] = str(data["_id"])

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to delete CTC details
@router.delete("/delete_ctc/{employee_id}")
async def delete_ctc(employee_id: str):
    try:
        # Find the document in the "employee_salaries_collection" based on the provided 'employee_id'
        result = employee_salaries_collection.find_one({"employee_id": employee_id})

        if not result:
            raise HTTPException(status_code=404, detail=f"CTC data for Employee with ID {employee_id} not found")

        # Delete the document from the "employee_salaries_collection"
        employee_salaries_collection.delete_one({"employee_id": employee_id})

        return {"message": f"CTC details for employee with ID {employee_id} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
