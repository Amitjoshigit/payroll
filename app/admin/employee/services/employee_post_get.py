from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from bson import ObjectId
import json


from ...DB_connection import db


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

router = APIRouter()


collection = db["employees"]

# Set custom JSONEncoder for MongoDB ObjectId serialization
json_encoder = CustomJSONEncoder()

# Define CRUD operations
@router.post("/", response_model=dict)
async def create_employee(employee: dict):
    result = collection.insert_one(employee)
    return JSONResponse(content={"id": str(result.inserted_id)}, status_code=201)

@router.get("/{employee_id}", response_model=dict)
async def read_employee(employee_id: str):
    employee = collection.find_one({"_id": ObjectId(employee_id)})
    if employee:
        return JSONResponse(content=json.loads(json_encoder.encode(employee)), status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

@router.get("/", response_model=list)
async def read_employees(skip: int = 0, limit: int = 10):
    employees = collection.find().skip(skip).limit(limit)
    return JSONResponse(content=json.loads(json_encoder.encode(list(employees))), status_code=200)

@router.put("{employee_id}", response_model=dict)
async def update_employee(employee_id: str, updated_employee: dict):
    result = collection.update_one({"_id": ObjectId(employee_id)}, {"$set": updated_employee})
    if result.modified_count == 1:
        return JSONResponse(content={"id": employee_id}, status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

@router.delete("/{employee_id}", response_model=dict)
async def delete_employee(employee_id: str):
    employee = collection.find_one({"_id": ObjectId(employee_id)})
    if employee:
        collection.delete_one({"_id": ObjectId(employee_id)})
        return JSONResponse(content=json.loads(json_encoder.encode(employee)), status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

