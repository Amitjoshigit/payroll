
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB setup
client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["payroll"]  # Change the database name as needed



employee_basic_collection = db["employee_basic"]
employee_salaries_collection = db["employee_salaries"]
employee_banks_collection = db["employee_banks"]
employee_documents_collection = db["employee_documents"]
employee_additional_details = db["additional_details"]
