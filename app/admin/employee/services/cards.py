
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse


from ...DB_connection import db


router = APIRouter()





# List of collections to check for total_ctc and total_monthly_ctc
collections_for_ctc = ["employee", "salaries"]


@router.get('/total_ctc_and_employees')
async def total_ctc_and_employees(month: str = Query(None, description="Select a month")):
    try:
        # Count total employees
        total_employees = db.employees.count_documents({})

        # Aggregate total CTC for all employees
        total_ctc = 0
        for collection_name in collections_for_ctc:
            collection = db[collection_name]
            
            pipeline_ctc = [
                {"$group": {"_id": None, "total_ctc": {"$sum": "$annual_ctc"}}}
            ]
            
            result_ctc = list(collection.aggregate(pipeline_ctc))
            
            if result_ctc:
                total_ctc += result_ctc[0].get("total_ctc", 0)

        # Aggregate total monthly CTC for all employees
        total_monthly_ctc = 0
        for collection_name in collections_for_ctc:
            collection = db[collection_name]
            
            pipeline_monthly_ctc = [
                {"$group": {"_id": None, "total_monthly_ctc": {"$sum": "$earning.monthly_ctc"}}}
            ]
            
            result_monthly_ctc = list(collection.aggregate(pipeline_monthly_ctc))
            
            if result_monthly_ctc:
                total_monthly_ctc += result_monthly_ctc[0].get("total_monthly_ctc", 0)

        return JSONResponse(content=[{"total_ctc": total_ctc, 
                                     "total_monthly_ctc": total_monthly_ctc,
                                     "total_employees": total_employees, 
                                     }])
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)















