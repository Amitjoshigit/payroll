


# Function for saving documents
from typing import List, Tuple
from fastapi import HTTPException, UploadFile
from app.admin.DB_connection import employee_documents_collection





async def update_employee_documents(employee_id :str, documents: List[Tuple[str, UploadFile, str]]):
    # Save documents to MongoDB under a single document
    try:
        if not documents:
            raise HTTPException(status_code=400, detail="No documents provided for the employee.")

        document_data = {
            "employee_id": employee_id, # Use employee_id as the _id field
            "documents": []
        }

        for document_type, document, document_number in documents:
            if document:
                validate_file(document, allowed_content_types={"image/png", "image/jpeg", "application/pdf"})
                content = await document.read()
                document_data["documents"].append({
                    "document_type": document_type,
                    "file_name": document.filename,
                    "content_type": document.content_type,
                    "data": content,
                    "document_number": document_number,
                })
        
        existing_document = await employee_documents_collection.find_one({"employee_id": employee_id})
        if existing_document:
            # Insert the new document
            await employee_documents_collection.update_one({"employee_id": employee_id}, {"$set": document_data}, upsert= True)
            print(f"Document updated successfully for employee {employee_id}.")
        else:
            print("No documents found for employee {employee_id}. ")
            raise HTTPException(status_code=404, detail=f"No documents found for employee {employee_id}.")

    except HTTPException as e:
        raise # Re-raise HTTPException to propagate it to the calling function
    except Exception as e:
        print(f"Error inserting document: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Function for validation . 
def validate_file(file: UploadFile, allowed_content_types: set):
    # Validate file type
    if file.content_type not in allowed_content_types:
        raise HTTPException(status_code=400, detail="Only PNG, JPEG or PDF files are allowed")

    # Validate file size
    max_file_size_kb = 200
    file_size = file.file.seek(0, 2)
    if file_size > max_file_size_kb * 1024:
        raise HTTPException(status_code=400, detail=f"File size should be less than {max_file_size_kb} KB")
    file.file.seek(0)  # Reset the file cursor to the beginning after checking the size
