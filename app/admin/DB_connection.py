import yaml 
from pymongo import MongoClient



# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["payroll"]  # Change the database name as needed