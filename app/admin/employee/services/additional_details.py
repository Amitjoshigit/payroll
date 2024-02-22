

from fastapi import APIRouter, Body, HTTPException,status
from pydantic import ValidationError 



from app.admin.DB_connection import employee_additional_details,employee_basic_collection
from app.admin.employee.schema.additional_detail import AdditionalDetailsAttributes

router = APIRouter()


# tested successfully working
@router.post("", response_model=dict)
async def create_additional_details(details: AdditionalDetailsAttributes):
    try:
        # Check if the employee_id exists in the employee collection
        if not employee_basic_collection.find_one({"employee_id": details.employee_id}):
            raise HTTPException(status_code=404, detail=f"Employee with ID {details.employee_id} not found")


    
        
        # Save the additional details to the additional_details_collection
        result = employee_additional_details.update_one({"employee_id": details.employee_id},{"$set":  details.dict()}, upsert=True)


        return {"message": "Additional details created", "employee_id": details.employee_id}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        return {"error": str(e)}


# need to test
@router.get("", response_model=AdditionalDetailsAttributes)
async def get_additional_details(employee_id: str = Body(..., title="Employee ID")):
    try:
        # Fetch data based on employee_id
        details = employee_additional_details.find_one({"employee_id": employee_id})
        if details:
            return details
        else:
            raise HTTPException(status_code=404, detail=f"Additional details for Employee ID {employee_id} not found")
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Invalid data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# @router.put("/api/additional-details/{details_id}", response_model=dict)
# async def update_additional_details(details_id: str, new_details: dict):
#     try:
#         validate_data(new_details)
#         result = db.additional_details.update_one({"_id": ObjectId(details_id)}, {"$set": new_details})
#         if result.matched_count > 0:
#             return {"message": "Additional details updated"}
#         raise HTTPException(status_code=404, detail="Details not found")
#     except ValueError as ve:
#         return JSONResponse(content={"error": str(ve)}, status_code=400)



# @router.delete("/api/additional-details/", response_model=dict)
# async def delete_additional_details(details_id: str):
#     result = db.additional_details.delete_one({"_id": ObjectId(details_id)})  # Convert to ObjectId
#     if result.deleted_count > 0:
#         return {"message": "Additional details deleted"}
#     raise HTTPException(status_code=404, detail="Details not found")






@router.put("/api/additional-details/{employee_id}", response_model=dict)
async def update_additional_details(employee_id: str, new_details: AdditionalDetailsAttributes):
    try:
        employee = employee_basic_collection.find_one({"employee_id": employee_id})
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with ID {employee_id} not found")

        details_dict = {"employee_id": employee_id, **new_details.dict()}
        result = employee_additional_details.replace_one({"employee_id": employee_id}, details_dict)


        if result.modified_count > 0:
            return {"message": "Additional details updated", "employee_id": employee_id}
        else:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Details not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/api/additional-details/{employee_id}", response_model=dict)
async def delete_additional_details(employee_id: str):
    result = employee_additional_details.delete_one({"employee_id": employee_id})

    if result.deleted_count > 0:
        return {"message": "Additional details deleted", "employee_id": employee_id}
    raise HTTPException(status_code=404, detail="Details not found")