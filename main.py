from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.admin.employee.routers.router import api_router 

app = FastAPI()



# Enable CORS
origins = ["*"]  # Set more restrictive origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)

