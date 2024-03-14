from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.admin.employee.routers.router import api_router as employee_router
from app.admin.DB_connection import db, client
from contextlib import asynccontextmanager



async def startup_event():
    

    # Check if the database exists, but don't attempt to create it again
    # if DATABASE_NAME not in await client.list_database_names():
    #     await db.command("create")  # This line was causing the error

    # Ensure collections exist
    collections = ["employee_basic", "employee_salaries", "employee_banks", "employee_documents", "additional_details"]
    for collection in collections:
        if collection not in await db.list_collection_names():
            await db.create_collection(collection)

    print("Database and collections ready for use")


async def shutdown():
    # Close MongoDB connection on shutdown
    client.close()
    print("MongoDB connection closed")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await startup_event()
    yield
    # Clean up the ML models and release the resources
    await shutdown()    



app = FastAPI(lifespan=lifespan)


# Enable CORS
origins = ["*"]  # Set more restrictive origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(employee_router,prefix="/employee",tags=["employee"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True)


# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.admin.employee.routers.router import api_router as employee_router
# from app.admin.DB_connection import db, client
# from contextlib import asynccontextmanager
# import time

# async def startup_event():
#     # Retry connection to MongoDB
#     retries = 5
#     for _ in range(retries):
#         try:
#             await client.admin.command("ping")
#             break
#         except Exception as e:
#             print(f"Error connecting to MongoDB: {e}")
#             print("Retrying...")
#             time.sleep(2)

#     # Ensure collections exist
#     collections = ["employee_basic", "employee_salaries", "employee_banks", "employee_documents", "additional_details"]
#     for collection in collections:
#         if collection not in await db.list_collection_names():
#             await db.create_collection(collection)

#     print("Database and collections ready for use")

# async def shutdown():
#     # Close MongoDB connection on shutdown
#     client.close()
#     print("MongoDB connection closed")

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Load the ML model
#     await startup_event()
#     yield
#     # Clean up the ML models and release the resources
#     await shutdown()    

# app = FastAPI(lifespan=lifespan)

# # Enable CORS
# origins = ["*"]  # Set more restrictive origins in production
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins, 
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(employee_router, prefix="/employee", tags=["employee"])

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
