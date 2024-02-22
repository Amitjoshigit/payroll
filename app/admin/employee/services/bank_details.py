
from fastapi import APIRouter, HTTPException



from app.admin.DB_connection import employee_banks_collection,employee_basic_collection
from app.admin.employee.schema.bank_details_schema import BankDetail,EmployeeBankDetails

router = APIRouter()



# POST method to create bank details for an employee
@router.post("", response_model=EmployeeBankDetails)
async def create_bank_details(employee_details: EmployeeBankDetails):
    # Check if the provided employee_id exists in the basic collection
    if not employee_basic_collection.find_one({"employee_id": employee_details.employee_id}):
        raise HTTPException(status_code=404, detail=f"Employee with ID {employee_details.employee_id} not found")
    
    # Convert bank details to a list of dictionaries
    bank_details = [bank_detail.dict() for bank_detail in employee_details.bank_details]
    
    # Create a document to store all bank details for the employee
    bank_document = {
        "employee_id": employee_details.employee_id,
        "bank_details": bank_details
    }
    
    # Insert the document into the bank collection
    inserted_doc = employee_banks_collection.update_one({"employee_id": employee_details.employee_id}, {"$set": bank_document}, upsert=True)
    
    # Return the inserted document
    return EmployeeBankDetails(**bank_document)

# GET method to retrieve bank details by employee_id
@router.get("/bank-details/{employee_id}", response_model=EmployeeBankDetails)
async def get_bank_details(employee_id: str):
    # Fetch the bank details document for the provided employee_id from the bank collection
    bank_document = employee_banks_collection.find_one({"employee_id": employee_id})
    
    # If the document is not found, raise a 404 HTTP exception
    if not bank_document:
        raise HTTPException(status_code=404, detail=f"Bank details not found for employee ID {employee_id}")
    
    # Convert bank document to EmployeeBankDetails model
    bank_details = EmployeeBankDetails(**bank_document)
    
    # Return the bank details document
    return bank_details

# PUT method to update bank details by employee_id
@router.put("/employee/bank-details/{employee_id}")
async def update_bank_details(employee_id: str, bank_detail: BankDetail):
    # Check if the provided employee_id exists in the Employee collection
    if employee_basic_collection.find_one({"employee_id": employee_id}):
        updated_detail = employee_banks_collection.update_one(
            {"employee_id": employee_id},
            {"$set": bank_detail.dict()}
        )
        if updated_detail.modified_count == 0:
            raise HTTPException(status_code=404, detail="Bank details not found")
        return {"message": "Bank details updated successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} not found")

# DELETE method to delete bank details by employee_id
@router.delete("/employee/bank-details/{employee_id}")
async def delete_bank_details(employee_id: str):
    # Check if the provided employee_id exists in the Employee collection
    if employee_basic_collection.find_one({"employee_id": employee_id}):
        deleted_detail = employee_banks_collection.delete_many({"employee_id": employee_id})
        if deleted_detail.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Bank details not found")
        return {"message": "Bank details deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} not found")