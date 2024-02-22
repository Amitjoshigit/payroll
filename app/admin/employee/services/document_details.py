
from fastapi import File, UploadFile, HTTPException, Form, APIRouter
from fastapi.responses import JSONResponse
import base64
from app.admin.employee.services.utility.document_details_util import  update_employee_documents, employee_documents_collection


router = APIRouter()


# Endpoint for image and text upload
@router.post("")
async def upload_employee_data(
    employee_id:str = Form(...), # Use employee_id in the URL
    aadhar_document: UploadFile = File(...),
    aadhar_number: str = Form(...),
    pan_document: UploadFile = File(...),
    pan_number: str = Form(...),
    esic_document: UploadFile = File(...),
    esic_number: str = Form(...),
    epfo_document: UploadFile = File(...),
    epfo_number: str = Form(...), 
    form16_document: UploadFile = File(...),
    form16_number: str = Form(...),
):
    
    # Inside upload_employee_data function
    documents = [
        ("aadhar", aadhar_document, aadhar_number),
        ("pan", pan_document, pan_number),
        ("esic", esic_document, esic_number),
        ("epfo", epfo_document, epfo_number),
        ("form16", form16_document, form16_number),
    ]
    try:
        await update_employee_documents(employee_id, documents)
        return JSONResponse(content={"message": "Data uploaded successfully", "employee_id": employee_id})
    except HTTPException as e:
        if e.status_code == 404:
            # Employee not found, return a specific response
            return JSONResponse(content={"error": f"No documents found for employee {employee_id}"}, status_code=404)
        else:
            # Other HTTPException, return a general error response
            return JSONResponse(content={"error": str(e)}, status_code=e.status_code)
    except Exception as e:
        # General exception, return a 500 Internal Server Error response
        return JSONResponse(content={"error": f"Internal Server Error: {str(e)}"}, status_code=500)





# Endpoint for calling employee document details with providing employee_id
@router.get("/get_employee_data/{employee_id}")
async def get_employee_data(employee_id: str):
    try:
        # Retrieve details for all employees
        employee_data = await employee_documents_collection.find_one({"employee_id": employee_id})

        if not employee_data:
            raise HTTPException(status_code=404, detail=f"No documents found for employee {employee_id}.")

        documents_info = []
        for document in employee_data.get("documents", []):
            document_data = {
                "document_type": document.get("document_type"),
                "file_name": document.get("file_name"),
                "content_type": document.get("content_type"),
                "document_number": document.get("document_number"),
                "data": base64.b64encode(document.get("data")).decode(),
            }
            documents_info.append(document_data)

        response_content = {"employee_id": employee_data.get("employee_id"), "documents": documents_info}
        print(f"Retrieved details for employee {employee_id}.")

        return JSONResponse(content=response_content)
    
    except HTTPException as e :
        raise # Re-raise HTTPException to propagate it to the calling function
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


# Endpoint for deleting employee documents
@router.delete("/employee_data/{employee_id}")
async def delete_employee_documents(employee_id: str):
    try:
        # Check if the employee exists
        existing_employee = await employee_documents_collection.find_one({"employee_id": employee_id})

        if not existing_employee:
            raise HTTPException(status_code=404, detail=f"No employee found with ID {employee_id}")

        # Update the employee data by removing the documents
        await employee_documents_collection.update_one({"employee_id": employee_id}, {"$set": {"documents": []}})

        return JSONResponse(content={"message": f"Document details for employee {employee_id} deleted successfully"})

    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
