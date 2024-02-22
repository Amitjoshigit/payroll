
from fastapi import APIRouter
from fastapi.responses import JSONResponse


from app.admin.DB_connection import employee_basic_collection,employee_salaries_collection


router = APIRouter()


# List of collections to check for total_ctc and total_monthly_ctc
collections_for_ctc = [employee_basic_collection,employee_salaries_collection]


@router.get('/total_ctc_and_employees')
async def total_ctc_and_employees():
    try:
        # Dummy logic to filter data based on selected month
        # This logic can be replaced with actual filtering based on month if required
        selected_month_data = await employee_salaries_collection.find().to_list(None)

        # Calculate total employees
        total_employees = len(selected_month_data)

        # Aggregate total CTC for all employees
        total_ctc = sum([employee.get("annual_ctc", 0) for employee in selected_month_data])

        # Aggregate total monthly CTC for all employees
        total_monthly_ctc = sum([employee.get("earning", {}).get("monthly_ctc", 0) for employee in selected_month_data])

        return JSONResponse(content=[{"total_ctc": total_ctc, 
                                      "total_monthly_ctc": total_monthly_ctc,
                                      "total_employees": total_employees}])
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)












