from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.report_router import router as report_router

app = FastAPI(title="AI Report Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(report_router, prefix="/api/report")
