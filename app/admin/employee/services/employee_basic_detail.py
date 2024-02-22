from fastapi import File, Form, UploadFile, HTTPException, APIRouter,HTTPException, status
from fastapi.responses import JSONResponse
from bson import Binary
from typing import List, Optional
import base64



from app.admin.DB_connection import employee_basic_collection, employee_documents_collection
from app.admin.employee.schema.employee_basic_detail_schema import Employee, EmployeeWithPhoto


router = APIRouter()



@router.post("")
async def create_employee(
    first_name : str = Form(),
    middle_name : Optional[str] = Form(),
    last_name : str = Form(),
    dob : str = Form(),
    gender : str = Form(),
    date_of_joining : str = Form(),
    blood_group : str = Form(),
    designation : str = Form(),
    employee_id : str = Form(),
    department : str = Form(),
    type_of_employee : str = Form(),
    ctc : Optional[float] = Form(default=0.0),
    address_line1 : str = Form(),
    address_line2 : str = Form(),
    differently_abled : str = Form(),
    personal_email : str = Form(),
    work_email : str = Form(),
    phone_number : str = Form(),
    alternate_phone_number : str = Form(),
    work_location : str = Form(),
    photo_content: UploadFile = File(...),
):
    """
    Create a new employee with the provided details.

    Parameters:
    - first_name (str): The first name of the employee
    - middle_name (Optional[str]): The middle name of the employee
    - last_name (str): The last name of the employee
    - dob (str): The date of birth of the employee
    - gender (str): The gender of the employee
    - date_of_joining (str): The date of joining of the employee
    - blood_group (str): The blood group of the employee
    - designation (str): The designation of the employee
    - employee_id (str): The unique ID of the employee
    - department (str): The department of the employee
    - type_of_employee (str): The type of employee
    - ctc (Optional[float]): The cost to company of the employee this is optional
    - address_line1 (str): The first address line of the employee
    - address_line2 (str): The second address line of the employee
    - differently_abled (str): Whether the employee is differently abled
    - personal_email (str): The personal email of the employee
    - work_email (str): The work email of the employee
    - phone_number (str): The phone number of the employee
    - alternate_phone_number (str): The alternate phone number of the employee
    - work_location (str): The work location of the employee
    - photo_content (UploadFile): The photo of the employee
    Returns:
    - JSONResponse: A JSON response with the message "Employee created successfully" and status code 201 if successful, or HTTPException with status code 422 if an error occurs.
    """
    try:
        emp_details = {
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "dob": dob,
            "gender": gender,
            "date_of_joining": date_of_joining,
            "blood_group": blood_group,
            "designation": designation,
            "employee_id": employee_id,
            "department": department,
            "type_of_employee": type_of_employee,
            "ctc": ctc,
            "address_line1": address_line1,
            "address_line2": address_line2,
            "differently_abled": differently_abled,
            "personal_email": personal_email,
            "work_email": work_email,
            "phone_number": phone_number,
            "alternate_phone_number": alternate_phone_number,
            "work_location": work_location
        }
        # Save employee details to "employees" collection
        result_employee = employee_basic_collection.update_one({"employee_id": employee_id}, {"$set":emp_details}, upsert=True)

        # Use the provided employee_id from the JSON body
        employee_id = emp_details["employee_id"]

        # Save employee photo to "employee_photos" collection under the specified employee_id
        photo_content = await photo_content.read()
        photo_data = Binary(base64.b64encode(photo_content))
        photo_document = {"employee_id": employee_id, "photo": photo_data}
        result_photo = employee_documents_collection.update_one({"employee_id": employee_id}, {"$set":photo_document}, upsert=True)

        # Return response
        return JSONResponse(content={"message": "Employee created successfully"}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

# Endpoint to get all employees with photos
@router.get("", response_model=List[EmployeeWithPhoto])
async def get_employees():
    employees_data = []
    async for employee in employee_basic_collection.find():
        employees_data.append(employee)
    employees_list = []

    for employee_data in employees_data:
        # Exclude MongoDB's default _id from the response
        employee_data.pop("_id", None)

        # Convert ObjectId to string for employee_id
        employee_id = str(employee_data["employee_id"])
        
        # Fetch employee photo from the employee_documents_collection
        photo_data = await employee_documents_collection.find_one({"employee_id": employee_id})

        # Combine employee details and photo content
        employee_details = {**employee_data, "employee_id": employee_id}

        # # Include photo_content in the response
        # if photo_data and "photo" in photo_data:
        #     # Check if photo_data["photo"] is already bytes-like
        #     if isinstance(photo_data["photo"], bytes):
        #         encoded_photo = base64.b64encode(photo_data["photo"])
        #     else:
        #         # If it's not bytes-like, encode it using UTF-8
        #         encoded_photo = base64.b64encode(photo_data["photo"].encode("utf-8"))

        #     # Convert bytes to a string
        #     photo_content = encoded_photo.decode("utf-8")

        #     employee_details["photo_content"] = photo_content
        # else:
        employee_details["photo_content"] = None

        employees_list.append(EmployeeWithPhoto(**employee_details))

    return employees_list

# # Endpoint to get employee by employee_id
# @router.get("/all_employees")
# async def get_all_employees():
#     # Fetch employee basic details from MongoDB collection
#     employee_data = await employee_basic_collection.find().to_list(None)
#     # Combine employee annual ctc and basic details
#     for employee in employee_data:
#         employee["_id"] = str(employee["_id"])
#         employee_id = employee["employee_id"]
#         # Fetch photo data for the employee
#         photo_data = await employee_documents_collection.find_one({"employee_id": employee_id})
#         if photo_data and "photo" in photo_data:
#             # Encode photo content to base64 and add to employee data
#             employee["photo_content"] = None #base64.b64encode(photo_data["photo"]).decode("utf-8")
#         else:
#             employee["photo_content"] = None
#         # Fetch annual ctc data for the employee
#         annual_ctc_data = await employee_salaries_collection.find_one({"employee_id": employee_id})
#         if annual_ctc_data:
#             employee["annual_ctc"] = annual_ctc_data["annual_ctc"]
#         else:
#             employee["annual_ctc"] = None
#     return employee_data

#     # if not employee_data:
    #     raise HTTPException(status_code=404, detail="Employee not found")

    # # Exclude MongoDB's default _id from the response
    # employee_data.pop("_id", None)

    # # Fetch employee photo from the employee_documents_collection
    # photo_data = employee_documents_collection.find_one({"employee_id": employee_id})

    # # Combine employee details and photo content
    # employee_details = {**employee_data, "employee_id": employee_id}
    
    # # Include photo_content in the response
    # if photo_data and "photo" in photo_data:
    #     employee_details["photo_content"] = base64.b64encode(photo_data["photo"]).decode("utf-8")
    # else:
    #     employee_details["photo_content"] = None

    # return EmployeeWithPhoto(**employee_details)
 
# Endpoint to update employee details by employee_id
@router.put("/employees/{employee_id}")
async def update_employee_by_id(employee_id: str, emp_details: Employee):
    # Update employee details in the employee_basic_collection
    result = employee_basic_collection.update_one(
        {"employee_id": employee_id},
        {"$set": emp_details.dict()},
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")

    return JSONResponse(content={"message": "Employee updated successfully"}, status_code=200)

# Endpoint to delete employee by employee_id
@router.delete("/employees/{employee_id}")
async def delete_employee_by_id(employee_id: str):
    # Delete employee details from the employee_basic_collection
    result_employee = employee_basic_collection.delete_one({"employee_id": employee_id})

    # Delete employee photo from the employee_documents_collection
    result_photo = employee_documents_collection.delete_one({"employee_id": employee_id})

    if result_employee.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")

    return JSONResponse(content={"message": "Employee deleted successfully"}, status_code=200)